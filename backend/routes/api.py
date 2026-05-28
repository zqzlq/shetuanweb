import os
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm.attributes import flag_modified

import oss_service

from models import db, SiteConfig, Page, Application, AdminUser, MemberUser, UserSubmission
from defaults import DEFAULT_SITE_CONFIG, DEFAULT_PAGES

api_bp = Blueprint('api', __name__)


# ─── Public: Site Config ───

@api_bp.route('/config', methods=['GET'])
def get_config():
    configs = SiteConfig.query.all()
    if not configs:
        return jsonify({'error': 'not_found', 'message': '站点配置不存在'}), 404
    result = {c.config_key: c.config_value for c in configs}
    result.pop('system', None)
    return jsonify(result)


# ─── Public: Pages ───

@api_bp.route('/pages', methods=['GET'])
def get_pages():
    pages = Page.query.all()
    return jsonify([{'slug': p.slug, 'title': p.title, 'updated_at': p.updated_at.isoformat() if p.updated_at else None} for p in pages])


@api_bp.route('/pages/<slug>', methods=['GET'])
def get_page(slug):
    page = Page.query.filter_by(slug=slug).first()
    if not page:
        return jsonify({'error': 'not_found', 'message': f'页面 {slug} 不存在'}), 404
    return jsonify(page.to_dict())


# ─── Public: Applications ───

@api_bp.route('/applications', methods=['POST'])
def submit_application():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'bad_request', 'message': '请求体为空'}), 400

    required = ['name', 'student_id', 'grade_major', 'phone', 'email', 'group_id', 'group_name', 'motivation']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': 'validation_error', 'message': f'缺少必填字段: {", ".join(missing)}'}), 400

    if len(data.get('motivation', '')) < 10:
        return jsonify({'error': 'validation_error', 'message': '申请动机至少 10 个字'}), 400

    # Rate limit
    from flask import current_app
    limit_minutes = current_app.config.get('APPLICATION_RATE_LIMIT_MINUTES', 10)
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=limit_minutes)
    ip = request.remote_addr

    dup = Application.query.filter(
        db.or_(
            Application.ip_address == ip,
            Application.email == data.get('email'),
            Application.phone == data.get('phone'),
        ),
        Application.created_at >= cutoff,
    ).first()
    if dup:
        return jsonify({'error': 'rate_limit', 'message': f'请勿重复提交，请 {limit_minutes} 分钟后再试'}), 429

    app_record = Application(
        name=data['name'],
        student_id=data['student_id'],
        grade_major=data['grade_major'],
        phone=data['phone'],
        email=data['email'],
        group_id=data['group_id'],
        group_name=data['group_name'],
        github_url=data.get('github_url'),
        portfolio_url=data.get('portfolio_url'),
        experience=data.get('experience'),
        motivation=data['motivation'],
        session=data.get('session'),
        ip_address=ip,
    )
    db.session.add(app_record)
    db.session.commit()

    # 飞书 Webhook 通知
    try:
        from application_flow import send_pending_application_card
        send_pending_application_card(app_record)
        db.session.commit()
    except Exception:
        current_app.logger.exception('飞书通知失败')

    return jsonify({'success': True, 'message': '申请已提交', 'application': app_record.to_dict()}), 201


# ─── User Auth ───

@api_bp.route('/auth/register', methods=['POST'])
def user_register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'bad_request', 'message': '请求体为空'}), 400

    required = ['username', 'email', 'password', 'name']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': 'validation_error', 'message': f'缺少必填字段: {", ".join(missing)}'}), 400

    if len(data['username']) < 2:
        return jsonify({'error': 'validation_error', 'message': '用户名至少 2 个字符'}), 400
    if len(data['password']) < 6:
        return jsonify({'error': 'validation_error', 'message': '密码至少 6 位'}), 400

    if MemberUser.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'conflict', 'message': '用户名已被使用'}), 400
    if MemberUser.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'conflict', 'message': '邮箱已被注册'}), 400

    user = MemberUser(
        username=data['username'],
        email=data['email'],
        name=data['name'],
        student_id=data.get('student_id', ''),
        phone=data.get('phone', ''),
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'success': True, 'message': '注册成功，请等待管理员审核', 'user': user.to_dict()}), 201


@api_bp.route('/auth/login', methods=['POST'])
def user_login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'bad_request', 'message': '请输入用户名和密码'}), 400

    user = MemberUser.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'auth_failed', 'message': '用户名或密码错误'}), 401

    if user.status == 'pending':
        return jsonify({'error': 'pending', 'message': '账号正在审核中，请等待管理员审核通过'}), 403
    if user.status == 'rejected':
        return jsonify({'error': 'rejected', 'message': '账号审核未通过'}), 403

    token = create_access_token(identity='user_' + str(user.id))
    return jsonify({'success': True, 'token': token, 'user': user.to_dict()})


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def user_me():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    user_id = int(identity.replace('user_', ''))
    user = MemberUser.query.get(user_id)
    if not user:
        return jsonify({'error': 'not_found', 'message': '用户不存在'}), 404
    return jsonify(user.to_dict())


@api_bp.route('/auth/profile', methods=['PATCH'])
@jwt_required()
def user_update_profile():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    user_id = int(identity.replace('user_', ''))
    user = MemberUser.query.get(user_id)
    if not user:
        return jsonify({'error': 'not_found', 'message': '用户不存在'}), 404

    data = request.get_json()
    for field in ['name', 'bio', 'avatar', 'social_links', 'student_id', 'phone']:
        if field in data:
            setattr(user, field, data[field])
    if 'group' in data:
        user.group_name = data['group']

    db.session.commit()
    return jsonify({'success': True, 'user': user.to_dict()})


@api_bp.route('/auth/password', methods=['PATCH'])
@jwt_required()
def user_change_password():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    user_id = int(identity.replace('user_', ''))
    user = MemberUser.query.get(user_id)
    if not user:
        return jsonify({'error': 'not_found', 'message': '用户不存在'}), 404

    data = request.get_json()
    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'bad_request', 'message': '缺少旧密码或新密码'}), 400
    if not user.check_password(data['old_password']):
        return jsonify({'error': 'auth_failed', 'message': '旧密码不正确'}), 401
    if len(data['new_password']) < 6:
        return jsonify({'error': 'validation_error', 'message': '新密码至少 6 位'}), 400

    user.set_password(data['new_password'])
    db.session.commit()
    return jsonify({'success': True, 'message': '密码已修改'})


@api_bp.route('/auth/submission', methods=['POST'])
@jwt_required()
def user_submit():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    user_id = int(identity.replace('user_', ''))
    user = MemberUser.query.get(user_id)
    if not user:
        return jsonify({'error': 'not_found', 'message': '用户不存在'}), 404

    data = request.get_json()
    if not data.get('type') or not data.get('title'):
        return jsonify({'error': 'bad_request', 'message': '缺少 type 或 title'}), 400

    sub = UserSubmission(
        user_id=user_id,
        type=data['type'],
        title=data['title'],
        description=data.get('description', ''),
        image=data.get('image', ''),
        data=data.get('data'),
    )
    db.session.add(sub)
    db.session.commit()

    return jsonify({'success': True, 'message': '提交成功，请等待管理员审核', 'submission': sub.to_dict()}), 201


@api_bp.route('/auth/submissions', methods=['GET'])
@jwt_required()
def user_submissions():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    user_id = int(identity.replace('user_', ''))
    subs = UserSubmission.query.filter_by(user_id=user_id).order_by(UserSubmission.created_at.desc()).all()
    return jsonify([s.to_dict() for s in subs])


@api_bp.route('/auth/submission/<int:sub_id>', methods=['DELETE'])
@jwt_required()
def user_delete_submission(sub_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    user_id = int(identity.replace('user_', ''))
    sub = UserSubmission.query.get(sub_id)
    if not sub:
        return jsonify({'error': 'not_found', 'message': '提交不存在'}), 404
    if sub.user_id != user_id:
        return jsonify({'error': 'forbidden', 'message': '无权删除'}), 403

    db.session.delete(sub)
    db.session.commit()
    return jsonify({'success': True, 'message': '提交已删除'})


# ─── Admin: Auth ───

@api_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'bad_request', 'message': '请输入用户名和密码'}), 400

    user = AdminUser.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'auth_failed', 'message': '用户名或密码错误'}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({'success': True, 'token': token, 'user': user.to_dict()})


@api_bp.route('/admin/me', methods=['GET'])
@jwt_required()
def admin_me():
    user = AdminUser.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'not_found', 'message': '用户不存在'}), 404
    return jsonify(user.to_dict())


# ─── Admin: Config ───

@api_bp.route('/admin/config', methods=['GET'])
@jwt_required()
def admin_get_config():
    configs = SiteConfig.query.all()
    return jsonify({c.config_key: c.config_value for c in configs})


@api_bp.route('/admin/config', methods=['PUT'])
@jwt_required()
def admin_update_config():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'bad_request', 'message': '请求体为空'}), 400

    for key, value in data.items():
        cfg = SiteConfig.query.filter_by(config_key=key).first()
        if cfg:
            cfg.config_value = value
        else:
            db.session.add(SiteConfig(config_key=key, config_value=value))

    db.session.commit()

    # 如果更新了 system 配置，热加载邮件和飞书配置
    if 'system' in data:
        try:
            from app import _load_mail_config
            _load_mail_config(current_app._get_current_object())
        except Exception:
            current_app.logger.exception('热加载邮件配置失败')

    return jsonify({'success': True, 'message': '配置已更新'})


@api_bp.route('/admin/config/<key>', methods=['PUT'])
@jwt_required()
def admin_update_config_key(key):
    data = request.get_json()
    cfg = SiteConfig.query.filter_by(config_key=key).first()
    if cfg:
        cfg.config_value = data
    else:
        db.session.add(SiteConfig(config_key=key, config_value=data))

    db.session.commit()
    return jsonify({'success': True, 'message': f'配置 {key} 已更新'})


# ─── Admin: Pages ───

@api_bp.route('/admin/pages', methods=['GET'])
@jwt_required()
def admin_get_pages():
    pages = Page.query.all()
    return jsonify([p.to_dict() for p in pages])


@api_bp.route('/admin/pages', methods=['POST'])
@jwt_required()
def admin_create_page():
    data = request.get_json()
    slug = data.get('slug')
    if not slug:
        return jsonify({'error': 'bad_request', 'message': '缺少 slug'}), 400
    if Page.query.filter_by(slug=slug).first():
        return jsonify({'error': 'conflict', 'message': f'页面 {slug} 已存在'}), 400

    page = Page(slug=slug, title=data.get('title', ''), content=data.get('content', {}))
    db.session.add(page)
    db.session.commit()
    return jsonify({'success': True, 'message': '页面已创建', 'page': page.to_dict()}), 201


@api_bp.route('/admin/pages/<slug>', methods=['GET'])
@jwt_required()
def admin_get_page(slug):
    page = Page.query.filter_by(slug=slug).first()
    if not page:
        return jsonify({'error': 'not_found', 'message': f'页面 {slug} 不存在'}), 404
    return jsonify(page.to_dict())


@api_bp.route('/admin/pages/<slug>', methods=['PUT'])
@jwt_required()
def admin_update_page(slug):
    data = request.get_json()
    page = Page.query.filter_by(slug=slug).first()

    if page:
        if 'title' in data:
            page.title = data['title']
        if 'content' in data:
            page.content = data['content']
    else:
        page = Page(slug=slug, title=data.get('title', slug), content=data.get('content', {}))
        db.session.add(page)

    db.session.commit()
    return jsonify({'success': True, 'message': '页面已更新', 'page': page.to_dict()})


@api_bp.route('/admin/pages/<slug>', methods=['DELETE'])
@jwt_required()
def admin_delete_page(slug):
    page = Page.query.filter_by(slug=slug).first()
    if not page:
        return jsonify({'error': 'not_found', 'message': f'页面 {slug} 不存在'}), 404

    db.session.delete(page)
    db.session.commit()
    return jsonify({'success': True, 'message': '页面已删除'})


@api_bp.route('/admin/pages/<slug>/reset', methods=['POST'])
@jwt_required()
def admin_reset_page(slug):
    default_data = DEFAULT_PAGES.get(slug)
    if not default_data:
        return jsonify({'error': 'not_found', 'message': f'无默认数据: {slug}'}), 404

    page = Page.query.filter_by(slug=slug).first()
    if page:
        page.title = default_data['title']
        page.content = default_data['content']
    else:
        page = Page(slug=slug, title=default_data['title'], content=default_data['content'])
        db.session.add(page)

    db.session.commit()
    return jsonify({'success': True, 'message': f'页面 {slug} 已重置', 'page': page.to_dict()})


# ─── Admin: Applications ───

@api_bp.route('/admin/applications', methods=['GET'])
@jwt_required()
def admin_get_applications():
    status = request.args.get('status', 'all')
    session = request.args.get('session', '')
    query = Application.query
    if status != 'all':
        query = query.filter_by(status=status)
    if session:
        query = query.filter_by(session=session)
    apps = query.order_by(Application.created_at.desc()).all()
    return jsonify([a.to_dict() for a in apps])


@api_bp.route('/admin/applications/<int:app_id>', methods=['PATCH'])
@jwt_required()
def admin_update_application(app_id):
    app_record = Application.query.get(app_id)
    if not app_record:
        return jsonify({'error': 'not_found', 'message': '申请不存在'}), 404

    data = request.get_json()
    old_status = app_record.status

    if 'status' in data:
        app_record.status = data['status']
        if data['status'] in ('approved', 'rejected'):
            app_record.processed_at = datetime.now(timezone.utc)
    if 'admin_note' in data:
        app_record.admin_note = data['admin_note']

    db.session.commit()

    # 状态变更时发送通知
    if 'status' in data and data['status'] != old_status:
        # 飞书状态更新通知
        try:
            from application_flow import send_status_update_card
            send_status_update_card(app_record)
            db.session.commit()
        except Exception:
            current_app.logger.exception('飞书状态更新通知失败')

        # 邮件通知
        if data['status'] in ('approved', 'rejected'):
            try:
                from application_flow import send_status_email
                group_link = data.get('group_link', None)
                qr_code_url = data.get('qr_code_url', None)
                send_status_email(app_record, 'result', group_link, qr_code_url)
                db.session.commit()
            except Exception:
                current_app.logger.exception('邮件发送失败')

    return jsonify({'success': True, 'message': '申请已更新', 'application': app_record.to_dict()})


@api_bp.route('/admin/applications/batch', methods=['POST'])
@jwt_required()
def admin_batch_update_applications():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'bad_request', 'message': '请求体为空'}), 400

    ids = data.get('ids', [])
    new_status = data.get('status')
    admin_note = data.get('admin_note')
    group_link = data.get('group_link')
    qr_code_url = data.get('qr_code_url')

    if not ids or not new_status:
        return jsonify({'error': 'bad_request', 'message': '缺少 ids 或 status'}), 400

    updated = []
    for app_id in ids:
        app_record = Application.query.get(app_id)
        if not app_record:
            continue

        old_status = app_record.status
        app_record.status = new_status
        if new_status in ('approved', 'rejected'):
            app_record.processed_at = datetime.now(timezone.utc)
        if admin_note:
            app_record.admin_note = admin_note

        db.session.commit()

        # 飞书通知
        if new_status != old_status:
            try:
                from application_flow import send_status_update_card
                send_status_update_card(app_record)
                db.session.commit()
            except Exception:
                current_app.logger.exception('飞书状态更新通知失败')

            # 邮件通知
            if new_status in ('approved', 'rejected'):
                try:
                    from application_flow import send_status_email
                    send_status_email(app_record, 'result', group_link, qr_code_url)
                    db.session.commit()
                except Exception:
                    current_app.logger.exception('邮件发送失败')

        updated.append(app_record.to_dict())

    return jsonify({'success': True, 'message': f'已更新 {len(updated)} 条申请', 'updated': updated})


@api_bp.route('/admin/applications/<int:app_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_application(app_id):
    app_record = Application.query.get(app_id)
    if not app_record:
        return jsonify({'error': 'not_found', 'message': '申请不存在'}), 404

    db.session.delete(app_record)
    db.session.commit()
    return jsonify({'success': True, 'message': '申请已删除'})


# ─── Admin: Users ───

@api_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def admin_get_users():
    status = request.args.get('status', 'all')
    query = MemberUser.query
    if status != 'all':
        query = query.filter_by(status=status)
    users = query.order_by(MemberUser.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users])


@api_bp.route('/admin/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def admin_update_user(user_id):
    user = MemberUser.query.get(user_id)
    if not user:
        return jsonify({'error': 'not_found', 'message': '用户不存在'}), 404

    data = request.get_json()
    if 'status' in data:
        user.status = data['status']

    db.session.commit()
    return jsonify({'success': True, 'message': '用户已更新', 'user': user.to_dict()})


@api_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user(user_id):
    user = MemberUser.query.get(user_id)
    if not user:
        return jsonify({'error': 'not_found', 'message': '用户不存在'}), 404
    # 如果该用户已同步到成员页，移除
    _remove_member_from_page(user.name or user.username)
    # 删除提交
    UserSubmission.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': '用户及关联提交已删除'})


@api_bp.route('/admin/users/batch', methods=['POST'])
@jwt_required()
def admin_batch_users():
    data = request.get_json()
    ids = data.get('ids', [])
    action = data.get('action', 'disable')
    if not ids:
        return jsonify({'error': 'bad_request', 'message': '缺少 ids'}), 400

    updated = 0
    for user_id in ids:
        user = MemberUser.query.get(user_id)
        if not user:
            continue
        if action == 'disable':
            user.status = 'rejected'
            updated += 1
        elif action == 'add-to-members':
            page = Page.query.filter_by(slug='members').first()
            if page and isinstance(page.content, dict):
                members = page.content.get('members', [])
                display_name = user.name or user.username
                if not any(m.get('name') == display_name for m in members):
                    members.append({
                        'name': display_name, 'role': '', 'group': '',
                        'avatar': user.avatar or '', 'description': user.bio or '',
                        'skills': [], 'socialLinks': user.social_links or [], 'projects': [],
                    })
                    page.content['members'] = members
                    flag_modified(page, 'content')
                    updated += 1
        elif action == 'delete':
            _remove_member_from_page(user.name or user.username)
            UserSubmission.query.filter_by(user_id=user_id).delete()
            db.session.delete(user)
            updated += 1

    db.session.commit()
    return jsonify({'success': True, 'message': f'已处理 {updated} 个用户'})


@api_bp.route('/admin/users/<int:user_id>/sync-member', methods=['POST'])
@jwt_required()
def admin_sync_user_to_member(user_id):
    user = MemberUser.query.get(user_id)
    if not user:
        return jsonify({'error': 'not_found', 'message': '用户不存在'}), 404

    # 找到 members 页面
    page = Page.query.filter_by(slug='members').first()
    if not page or not isinstance(page.content, dict):
        return jsonify({'error': 'not_found', 'message': '成员页面不存在'}), 404

    members = page.content.get('members', [])
    display_name = user.name or user.username
    # 检查是否已存在同名成员
    if any(m.get('name') == display_name for m in members):
        return jsonify({'error': 'conflict', 'message': '该用户已在成员列表中'}), 400

    members.append({
        'name': display_name,
        'role': '',
        'group': user.group_name or '',
        'avatar': user.avatar or '',
        'description': user.bio or '',
        'skills': [],
        'socialLinks': user.social_links or [],
        'projects': [],
    })
    page.content['members'] = members
    flag_modified(page, 'content')
    db.session.commit()
    return jsonify({'success': True, 'message': f'{user.name} 已添加到成员页面'})


# ─── Admin: Submissions ───

@api_bp.route('/admin/submissions', methods=['GET'])
@jwt_required()
def admin_get_submissions():
    status = request.args.get('status', 'all')
    query = UserSubmission.query
    if status != 'all':
        query = query.filter_by(status=status)
    subs = query.order_by(UserSubmission.created_at.desc()).all()
    return jsonify([s.to_dict() for s in subs])


@api_bp.route('/admin/submissions/<int:sub_id>', methods=['PATCH'])
@jwt_required()
def admin_update_submission(sub_id):
    sub = UserSubmission.query.get(sub_id)
    if not sub:
        return jsonify({'error': 'not_found', 'message': '提交不存在'}), 404

    data = request.get_json()
    if 'status' in data:
        sub.status = data['status']

    db.session.commit()

    # 审核通过后自动同步到页面
    if 'status' in data and data['status'] == 'approved':
        sync_submission_to_page(sub)

    return jsonify({'success': True, 'message': '提交已更新', 'submission': sub.to_dict()})


def _remove_member_from_page(name):
    """从成员页面删除同名成员"""
    try:
        page = Page.query.filter_by(slug='members').first()
        if page and isinstance(page.content, dict):
            members = page.content.get('members', [])
            before = len(members)
            members = [m for m in members if m.get('name') != name]
            if len(members) < before:
                page.content['members'] = members
                flag_modified(page, 'content')
                db.session.commit()
    except Exception:
        pass


def sync_submission_to_page(sub):
    """将审核通过的提交同步到对应页面"""
    page = Page.query.filter_by(slug='projects').first()
    if not page or not isinstance(page.content, dict):
        return

    extra = sub.data or {}

    # slug 为空时使用标题作为 slug
    award_slug = extra.get('slug') or sub.title
    project_slug = extra.get('slug') or sub.title

    if sub.type == 'award':
        awards = page.content.get('awards', {})
        items = awards.get('items', [])
        if not any(a.get('slug') == award_slug for a in items if award_slug):
            items.append({
                'slug': award_slug,
                'title': extra.get('title', sub.title),
                'shortDesc': extra.get('shortDesc', ''),
                'description': extra.get('description', ''),
                'longDescription': extra.get('longDescription', ''),
                'level': extra.get('level', ''),
                'date': extra.get('date', ''),
                'category': extra.get('category', ''),
                'participants': extra.get('participants', []),
                'projectSlug': extra.get('projectSlug', ''),
                'image': extra.get('image', sub.image or ''),
                'screenshots': extra.get('screenshots', []),
            })
            awards['items'] = items
            page.content['awards'] = awards

    elif sub.type == 'project':
        projects = page.content.get('projects', [])
        if not any(p.get('slug') == project_slug for p in projects if project_slug):
            projects.append({
                'name': extra.get('name', sub.title),
                'slug': project_slug,
                'category': extra.get('category', ''),
                'description': extra.get('description', ''),
                'longDescription': extra.get('longDescription', ''),
                'coverClass': extra.get('coverClass', 'aurora'),
                'coverImage': extra.get('coverImage', sub.image or ''),
                'screenshots': extra.get('screenshots', []),
                'techStack': extra.get('techStack', []),
                'githubUrl': extra.get('githubUrl', ''),
                'link': extra.get('link', ''),
                'status': 'active',
                'featured': False,
                'contributors': [],
            })
            page.content['projects'] = projects

    flag_modified(page, 'content')
    db.session.commit()


@api_bp.route('/admin/submissions/<int:sub_id>/sync', methods=['POST'])
@jwt_required()
def admin_sync_submission(sub_id):
    sub = UserSubmission.query.get(sub_id)
    if not sub:
        return jsonify({'error': 'not_found', 'message': '提交不存在'}), 404

    sync_submission_to_page(sub)
    return jsonify({'success': True, 'message': '已同步到页面'})


# ─── Admin: Image Upload ───

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


@api_bp.route('/admin/delete-image', methods=['POST'])
@jwt_required()
def admin_delete_image():
    data = request.get_json()
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'bad_request', 'message': '缺少 url'}), 400

    # 尝试从 URL 中提取 OSS key 并删除
    try:
        import oss_service
        cfg = SiteConfig.query.filter_by(config_key='system').first()
        system_cfg = cfg.config_value if cfg and isinstance(cfg.config_value, dict) else {}

        cdn_url = (system_cfg.get('aliyunOssCdnUrl') or '').strip()
        if cdn_url and url.startswith(cdn_url):
            key = url[len(cdn_url):].lstrip('/')
        else:
            # 从 bucket URL 中提取 key: https://{bucket}.{endpoint}/{key}
            from urllib.parse import urlparse
            parsed = urlparse(url)
            path = parsed.path.lstrip('/')
            if '/' in path:
                key = path
            else:
                key = path

        if key:
            oss_service.delete_file(key)
    except Exception:
        current_app.logger.exception('OSS 删除失败')

    # 同时尝试删除本地文件
    try:
        if url.startswith('/uploads/'):
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], url.replace('/uploads/', ''))
            if os.path.exists(filepath):
                os.remove(filepath)
    except Exception:
        pass

    return jsonify({'success': True, 'message': '图片已删除'})


@api_bp.route('/admin/upload-image', methods=['POST'])
@jwt_required()
def admin_upload_image():
    file = request.files.get('file')
    if not file or not file.filename:
        return jsonify({'error': 'bad_request', 'message': '未选择文件'}), 400

    ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({'error': 'bad_request', 'message': f'不支持的格式，仅允许: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}'}), 400

    filename = f"{uuid4().hex}{ext}"
    file_bytes = file.read()

    # 尝试 OSS 上传
    oss_key = f"images/{filename}"
    oss_url = oss_service.upload_file(oss_key, file_bytes)
    if oss_url:
        return jsonify({'success': True, 'message': '已上传到 OSS', 'filename': filename, 'url': oss_url})

    # 回退到本地存储
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(file_bytes)

    return jsonify({'success': True, 'message': '已保存到本地', 'filename': filename, 'url': f'/uploads/{filename}'})


# ─── Admin: Data Management ───

@api_bp.route('/admin/export', methods=['GET'])
@jwt_required()
def admin_export():
    configs = {c.config_key: c.config_value for c in SiteConfig.query.all()}
    pages = {p.slug: {'title': p.title, 'content': p.content} for p in Page.query.all()}
    return jsonify({'config': configs, 'pages': pages})


@api_bp.route('/admin/import', methods=['POST'])
@jwt_required()
def admin_import():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'bad_request', 'message': '请求体为空'}), 400

    for key, value in data.get('config', {}).items():
        cfg = SiteConfig.query.filter_by(config_key=key).first()
        if cfg:
            cfg.config_value = value
        else:
            db.session.add(SiteConfig(config_key=key, config_value=value))

    for slug, page_data in data.get('pages', {}).items():
        page = Page.query.filter_by(slug=slug).first()
        if page:
            page.title = page_data.get('title', page.title)
            page.content = page_data.get('content', page.content)
        else:
            db.session.add(Page(slug=slug, title=page_data.get('title', ''), content=page_data.get('content', {})))

    db.session.commit()
    return jsonify({'success': True, 'message': '数据已导入'})


@api_bp.route('/admin/reset-all', methods=['POST'])
@jwt_required()
def admin_reset_all():
    SiteConfig.query.delete()
    Page.query.delete()

    for key, value in DEFAULT_SITE_CONFIG.items():
        db.session.add(SiteConfig(config_key=key, config_value=value))
    for slug, data in DEFAULT_PAGES.items():
        db.session.add(Page(slug=slug, title=data['title'], content=data['content']))

    db.session.commit()
    return jsonify({'success': True, 'message': '所有内容已重置为默认值'})
