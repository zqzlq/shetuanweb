import os
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm.attributes import flag_modified

import oss_service

from models import db, SiteConfig, Page, Application, AdminUser, MemberUser, UserSubmission, ContactMessage, Resource, ResourceVersion, ResourceLog, ResourceComment
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


# ─── Public: Contact ───

@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'bad_request', 'message': '请求体为空'}), 400

    is_anonymous = data.get('is_anonymous', False)

    if not is_anonymous:
        required = ['name', 'email', 'subject', 'message']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({'error': 'validation_error', 'message': f'缺少必填字段: {", ".join(missing)}'}), 400
    else:
        if not data.get('subject') or not data.get('message'):
            return jsonify({'error': 'validation_error', 'message': '请填写主题和留言内容'}), 400

    if len(data.get('message', '')) < 5:
        return jsonify({'error': 'validation_error', 'message': '留言内容至少 5 个字'}), 400

    # Rate limit
    limit_minutes = 5
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=limit_minutes)
    ip = request.remote_addr

    dup = ContactMessage.query.filter(
        ContactMessage.ip_address == ip,
        ContactMessage.created_at >= cutoff,
    ).first()
    if dup:
        return jsonify({'error': 'rate_limit', 'message': f'请勿重复提交，请 {limit_minutes} 分钟后再试'}), 429

    msg = ContactMessage(
        name=data.get('name', '匿名用户') if not is_anonymous else '匿名用户',
        email=data.get('email', '') if not is_anonymous else '',
        phone=data.get('phone'),
        subject=data['subject'],
        message=data['message'],
        ip_address=ip,
        is_anonymous=is_anonymous,
    )
    db.session.add(msg)
    db.session.commit()

    # 飞书通知
    try:
        from application_flow import send_contact_notification
        send_contact_notification(msg)
    except Exception:
        current_app.logger.exception('飞书留言通知失败')

    return jsonify({'success': True, 'message': '留言已提交，我们会尽快回复'}), 201


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


# ─── Admin: Contact Messages ───

@api_bp.route('/admin/contact-messages', methods=['GET'])
@jwt_required()
def admin_get_contact_messages():
    status = request.args.get('status', 'all')
    query = ContactMessage.query
    if status != 'all':
        query = query.filter_by(status=status)
    messages = query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([m.to_dict() for m in messages])


@api_bp.route('/admin/contact-messages/<int:msg_id>', methods=['PATCH'])
@jwt_required()
def admin_update_contact_message(msg_id):
    msg = ContactMessage.query.get(msg_id)
    if not msg:
        return jsonify({'error': 'not_found', 'message': '留言不存在'}), 404

    data = request.get_json()
    if 'status' in data:
        msg.status = data['status']
        if data['status'] == 'read' and not msg.read_at:
            msg.read_at = datetime.now(timezone.utc)
    if 'admin_note' in data:
        msg.admin_note = data['admin_note']
    if 'reply' in data:
        msg.reply = data['reply']
        if data['reply']:
            msg.replied_at = datetime.now(timezone.utc)
            msg.status = 'replied'

    db.session.commit()
    return jsonify({'success': True, 'message': '留言已更新', 'contact_message': msg.to_dict()})


@api_bp.route('/admin/contact-messages/<int:msg_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_contact_message(msg_id):
    msg = ContactMessage.query.get(msg_id)
    if not msg:
        return jsonify({'error': 'not_found', 'message': '留言不存在'}), 404

    db.session.delete(msg)
    db.session.commit()
    return jsonify({'success': True, 'message': '留言已删除'})


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


# ─── Resources: Constants ───

ALLOWED_RESOURCE_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'md', 'csv', 'rtf',
    'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'bmp', 'ico',
    'zip', 'rar', '7z', 'tar', 'gz', 'bz2',
    'py', 'js', 'ts', 'jsx', 'tsx', 'html', 'css', 'json', 'yaml', 'yml', 'xml',
    'sql', 'sh', 'bat', 'java', 'c', 'cpp', 'go', 'rs',
    'mp3', 'wav', 'mp4', 'webm', 'ogg',
    'psd', 'ai', 'sketch', 'fig',
}

TEXT_PREVIEW_EXTENSIONS = {
    'txt', 'md', 'csv', 'json', 'xml', 'yaml', 'yml',
    'py', 'js', 'ts', 'jsx', 'tsx', 'html', 'css', 'sql', 'sh', 'bat',
    'java', 'c', 'cpp', 'go', 'rs', 'rtf',
}

IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'bmp', 'ico'}
PDF_EXTENSIONS = {'pdf'}
MARKDOWN_EXTENSIONS = {'md'}




def _log_action(resource_id, resource_name, action, user_id=None, detail=None):
    """记录资源操作日志"""
    try:
        log = ResourceLog(
            resource_id=resource_id,
            resource_name=resource_name,
            action=action,
            user_id=user_id,
            detail=detail,
        )
        db.session.add(log)
    except Exception:
        pass


def _get_current_user_id():
    """从 JWT 获取当前用户 ID（支持普通用户和管理员）"""
    identity = get_jwt_identity()
    if isinstance(identity, str) and identity.startswith('user_'):
        return int(identity.replace('user_', ''))
    return None


def _require_admin():
    """验证管理员身份，返回 AdminUser 或 None"""
    identity = get_jwt_identity()
    if isinstance(identity, str) and identity.startswith('user_'):
        return None
    try:
        return AdminUser.query.get(int(identity))
    except (ValueError, TypeError):
        return None


def _get_ancestor_chain(resource):
    """获取面包屑祖先链"""
    ancestors = []
    current = resource.parent
    while current:
        ancestors.insert(0, {'id': current.id, 'name': current.name})
        current = current.parent
    return ancestors


# ─── Resources: User API ───

@api_bp.route('/resources/tree', methods=['GET'])
@jwt_required()
def get_resource_tree():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    folders = Resource.query.filter_by(is_folder=True, status='approved', parent_id=None).order_by(Resource.name).all()
    result = []
    for f in folders:
        children_count = Resource.query.filter_by(parent_id=f.id, status='approved').count()
        result.append({
            'id': f.id,
            'name': f.name,
            'description': f.description,
            'children_count': children_count,
            'created_at': f.created_at.isoformat() if f.created_at else None,
        })
    return jsonify({'folders': result})


@api_bp.route('/resources/stats', methods=['GET'])
@jwt_required()
def get_resource_stats():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    parent_id = request.args.get('parent_id', type=int)

    def count_recursive(fid):
        total_files = 0
        total_size = 0
        children = Resource.query.filter_by(parent_id=fid, status='approved').all()
        for c in children:
            if c.is_folder:
                f, s = count_recursive(c.id)
                total_files += f
                total_size += s
            else:
                total_files += 1
                total_size += (c.file_size or 0)
        return total_files, total_size

    total_files, total_size = count_recursive(parent_id)
    return jsonify({'total_files': total_files, 'total_size': total_size})


@api_bp.route('/resources/folders', methods=['GET'])
@jwt_required()
def get_folders():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    folders = Resource.query.filter_by(is_folder=True, status='approved').order_by(Resource.name).all()
    result = [{'id': f.id, 'name': f.name, 'parent_id': f.parent_id} for f in folders]
    return jsonify({'folders': result})


@api_bp.route('/resources/tags', methods=['GET'])
@jwt_required()
def get_resource_tags():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resources = Resource.query.filter_by(status='approved').filter(Resource.tags.isnot(None)).all()
    tag_counts = {}
    for r in resources:
        if r.tags:
            for tag in r.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])
    return jsonify({'tags': [{'name': t, 'count': c} for t, c in sorted_tags]})


@api_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    parent_id = request.args.get('parent_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()
    tag = request.args.get('tag', '').strip()

    query = Resource.query.filter_by(status='approved')

    # 搜索时跨所有文件夹，不搜索时按当前文件夹过滤
    if search:
        query = query.filter(
            db.or_(
                Resource.name.ilike(f'%{search}%'),
                Resource.description.ilike(f'%{search}%'),
                Resource.original_name.ilike(f'%{search}%'),
            )
        )
    elif parent_id:
        query = query.filter_by(parent_id=parent_id)
    else:
        query = query.filter_by(parent_id=None)

    if tag:
        query = query.filter(Resource.tags.contains(f'"{tag}"'))

    # 文件夹排前面，然后按时间倒序
    query = query.order_by(Resource.is_folder.desc(), Resource.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # 面包屑
    breadcrumb = []
    if parent_id:
        parent = Resource.query.get(parent_id)
        if parent:
            breadcrumb = _get_ancestor_chain(parent) + [{'id': parent.id, 'name': parent.name}]

    items = [r.to_dict() for r in pagination.items]

    # 搜索时为每个结果附加文件夹路径
    if search:
        for item, resource in zip(items, pagination.items):
            item['folder_path'] = '/'.join(a['name'] for a in _get_ancestor_chain(resource)) if resource.parent_id else ''

    return jsonify({
        'items': items,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': per_page,
        'pages': pagination.pages,
        'breadcrumb': breadcrumb,
    })


@api_bp.route('/resources/<int:resource_id>', methods=['GET'])
@jwt_required()
def get_resource(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.status != 'approved':
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    data = resource.to_dict()
    data['breadcrumb'] = _get_ancestor_chain(resource)
    return jsonify(data)


@api_bp.route('/resources/upload', methods=['POST'])
@jwt_required()
def upload_resource():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    user_id = int(identity.replace('user_', ''))

    file = request.files.get('file')
    if not file or not file.filename:
        return jsonify({'error': 'validation', 'message': '请选择文件'}), 400

    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in ALLOWED_RESOURCE_EXTENSIONS:
        return jsonify({'error': 'validation', 'message': f'不支持的文件类型: .{ext}'}), 400

    parent_id = request.form.get('parent_id', type=int)
    tags_raw = request.form.get('tags', '').strip()
    description = request.form.get('description', '').strip()

    import json
    tags = json.loads(tags_raw) if tags_raw else []

    file_bytes = file.read()
    file_size = len(file_bytes)
    filename = f"{uuid4().hex}.{ext}"
    oss_key = f"resources/{filename}"

    oss_url = oss_service.upload_file(oss_key, file_bytes)
    if oss_url:
        file_url = oss_url
        stored_oss_key = oss_key
    else:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        resource_dir = os.path.join(upload_folder, 'resources')
        os.makedirs(resource_dir, exist_ok=True)
        filepath = os.path.join(resource_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(file_bytes)
        file_url = f'/uploads/resources/{filename}'
        stored_oss_key = None

    import mimetypes
    mime_type = mimetypes.guess_type(file.filename)[0]

    # 检查同文件夹下是否有同名文件，有则创建版本记录
    existing = Resource.query.filter_by(
        name=file.filename, parent_id=parent_id, is_folder=False, status='approved'
    ).first()

    if existing:
        # 保存旧版本
        last_version = ResourceVersion.query.filter_by(resource_id=existing.id).order_by(ResourceVersion.version.desc()).first()
        new_ver = (last_version.version + 1) if last_version else 2
        version_record = ResourceVersion(
            resource_id=existing.id,
            version=new_ver - 1,
            file_url=existing.file_url,
            oss_key=existing.oss_key,
            original_name=existing.original_name,
            file_size=existing.file_size,
            file_ext=existing.file_ext,
            uploader_id=existing.uploader_id,
        )
        db.session.add(version_record)

        # 更新现有资源
        existing.file_url = file_url
        existing.oss_key = stored_oss_key
        existing.original_name = file.filename
        existing.file_size = file_size
        existing.file_ext = ext
        existing.mime_type = mime_type
        existing.uploader_id = user_id
        existing.updated_at = datetime.now(timezone.utc)
        if tags:
            existing.tags = tags
        if description:
            existing.description = description
        db.session.commit()

        return jsonify({'success': True, 'message': f'文件已更新（版本 {new_ver}）', 'resource': existing.to_dict()})

    resource = Resource(
        name=file.filename,
        is_folder=False,
        parent_id=parent_id,
        tags=tags if tags else None,
        description=description if description else None,
        file_url=file_url,
        oss_key=stored_oss_key,
        original_name=file.filename,
        file_size=file_size,
        mime_type=mime_type,
        file_ext=ext,
        uploader_id=user_id,
        status='approved',
    )
    db.session.add(resource)
    db.session.flush()
    _log_action(resource.id, resource.name, 'upload', user_id)
    db.session.commit()

    return jsonify({'success': True, 'message': '上传成功', 'resource': resource.to_dict()}), 201


@api_bp.route('/resources/folder', methods=['POST'])
@jwt_required()
def create_folder():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    user_id = int(identity.replace('user_', ''))

    data = request.get_json()
    if not data or not data.get('name', '').strip():
        return jsonify({'error': 'validation', 'message': '请输入文件夹名称'}), 400

    name = data['name'].strip()
    parent_id = data.get('parent_id')
    description = data.get('description', '').strip()

    folder = Resource(
        name=name,
        is_folder=True,
        parent_id=parent_id,
        description=description if description else None,
        uploader_id=user_id,
        status='approved',
    )
    db.session.add(folder)
    db.session.commit()

    return jsonify({'success': True, 'message': '文件夹创建成功', 'resource': folder.to_dict()}), 201


@api_bp.route('/resources/<int:resource_id>/download', methods=['GET'])
@jwt_required()
def download_resource(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.is_folder or resource.status != 'approved':
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    resource.download_count += 1
    user_id = int(identity.replace('user_', ''))
    _log_action(resource.id, resource.name, 'download', user_id)
    db.session.commit()

    # 读取文件并代理返回
    file_bytes = None
    content_type = 'application/octet-stream'
    if resource.file_url.startswith('/uploads/'):
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], resource.file_url.replace('/uploads/', ''))
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                file_bytes = f.read()
    else:
        import urllib.request as urlreq
        try:
            with urlreq.urlopen(resource.file_url, timeout=30) as resp:
                file_bytes = resp.read()
                ct = resp.headers.get('Content-Type', '')
                if ct: content_type = ct
        except Exception:
            pass

    if not file_bytes:
        return jsonify({'error': 'fetch_failed', 'message': '无法获取文件'}), 500

    from flask import Response
    from urllib.parse import quote
    # 使用当前显示名称，如果没有扩展名则从原始名补上
    display = (resource.name or resource.original_name).strip()
    if resource.file_ext and not display.lower().endswith('.' + resource.file_ext.lower()):
        fname = display + '.' + resource.file_ext
    else:
        fname = display
    return Response(
        file_bytes,
        content_type=content_type,
        headers={
            'Content-Disposition': f"attachment; filename*=UTF-8''{quote(fname)}",
            'Content-Length': str(len(file_bytes)),
        }
    )


@api_bp.route('/resources/batch-download', methods=['POST'])
@jwt_required()
def batch_download_resources():
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    data = request.get_json()
    file_ids = data.get('file_ids', [])
    folder_ids = data.get('folder_ids', [])
    if not file_ids and not folder_ids:
        return jsonify({'error': 'validation', 'message': '请选择文件'}), 400

    # 收集直接选中的文件
    files_to_zip = []
    if file_ids:
        direct_files = Resource.query.filter(
            Resource.id.in_(file_ids),
            Resource.is_folder == False,
            Resource.status == 'approved',
        ).all()
        files_to_zip.extend([(f, '') for f in direct_files])

    # 递归收集文件夹内的文件
    def collect_folder_files(folder_id, prefix=''):
        children = Resource.query.filter_by(parent_id=folder_id, status='approved').all()
        for child in children:
            if child.is_folder:
                collect_folder_files(child.id, prefix + child.name + '/')
            else:
                files_to_zip.append((child, prefix))

    for fid in folder_ids:
        folder = Resource.query.get(fid)
        if folder and folder.is_folder:
            collect_folder_files(folder.id, folder.name + '/')

    if not files_to_zip:
        return jsonify({'error': 'not_found', 'message': '没有可下载的文件'}), 404

    import zipfile
    import io

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        name_counts = {}
        for r, prefix in files_to_zip:
            fname = prefix + (r.original_name or r.name)
            if fname in name_counts:
                name_counts[fname] += 1
                base, ext = os.path.splitext(fname)
                fname = f"{base}_{name_counts[fname]}{ext}"
            else:
                name_counts[fname] = 0

            file_bytes = None
            if r.file_url.startswith('/uploads/'):
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], r.file_url.replace('/uploads/', ''))
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        file_bytes = f.read()
            else:
                try:
                    import urllib.request as urlreq
                    with urlreq.urlopen(r.file_url, timeout=30) as resp:
                        file_bytes = resp.read()
                except Exception:
                    pass

            if file_bytes:
                zf.writestr(fname, file_bytes)
                r.download_count += 1

    db.session.commit()

    zip_buffer.seek(0)
    from flask import Response
    from urllib.parse import quote
    zip_name = f"resources_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.zip"
    encoded_name = quote(zip_name)

    return Response(
        zip_buffer.getvalue(),
        content_type='application/zip',
        headers={
            'Content-Disposition': f"attachment; filename*=UTF-8''{encoded_name}",
        }
    )


@api_bp.route('/resources/<int:resource_id>/versions', methods=['GET'])
@jwt_required()
def get_resource_versions(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.status != 'approved':
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    versions = ResourceVersion.query.filter_by(resource_id=resource_id).order_by(ResourceVersion.version.desc()).all()
    return jsonify({
        'current': resource.to_dict(),
        'versions': [v.to_dict() for v in versions],
    })


@api_bp.route('/resources/<int:resource_id>/versions/<int:version_id>/restore', methods=['POST'])
@jwt_required()
def restore_version(resource_id, version_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    version = ResourceVersion.query.get(version_id)
    if not resource or not version or version.resource_id != resource_id:
        return jsonify({'error': 'not_found', 'message': '版本不存在'}), 404

    # 保存当前版本
    last_version = ResourceVersion.query.filter_by(resource_id=resource_id).order_by(ResourceVersion.version.desc()).first()
    new_ver = (last_version.version + 1) if last_version else 2
    current_version = ResourceVersion(
        resource_id=resource_id,
        version=new_ver,
        file_url=resource.file_url,
        oss_key=resource.oss_key,
        original_name=resource.original_name,
        file_size=resource.file_size,
        file_ext=resource.file_ext,
        uploader_id=resource.uploader_id,
    )
    db.session.add(current_version)

    # 恢复选中的版本
    resource.file_url = version.file_url
    resource.oss_key = version.oss_key
    resource.original_name = version.original_name
    resource.file_size = version.file_size
    resource.file_ext = version.file_ext
    resource.uploader_id = int(identity.replace('user_', ''))
    resource.updated_at = datetime.now(timezone.utc)

    db.session.commit()
    return jsonify({'success': True, 'message': f'已恢复到版本 {version.version}', 'resource': resource.to_dict()})


@api_bp.route('/resources/<int:resource_id>', methods=['PATCH'])
@jwt_required()
def update_resource(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.status != 'approved':
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    data = request.get_json()
    if 'name' in data:
        resource.name = data['name'].strip()
    if 'tags' in data:
        resource.tags = data['tags'] if isinstance(data['tags'], list) else []
    if 'description' in data:
        resource.description = data['description'] if data['description'] else None

    db.session.commit()
    return jsonify({'success': True, 'message': '已更新', 'resource': resource.to_dict()})


@api_bp.route('/resources/<int:resource_id>/share', methods=['POST'])
@jwt_required()
def create_share_link(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.status != 'approved':
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    if not resource.share_token:
        resource.share_token = uuid4().hex
        db.session.commit()

    return jsonify({'success': True, 'token': resource.share_token, 'is_folder': resource.is_folder})


@api_bp.route('/resources/<int:resource_id>/unshare', methods=['POST'])
@jwt_required()
def remove_share_link(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    resource.share_token = None
    db.session.commit()
    return jsonify({'success': True, 'message': '已取消分享'})


@api_bp.route('/share/<token>', methods=['GET'])
def get_shared_resource(token):
    resource = Resource.query.filter_by(share_token=token, status='approved').first()
    if not resource:
        return jsonify({'error': 'not_found', 'message': '分享链接无效或已过期'}), 404

    data = {
        'id': resource.id,
        'name': resource.original_name or resource.name,
        'is_folder': resource.is_folder,
        'file_size': resource.file_size,
        'file_ext': resource.file_ext,
        'file_url': resource.file_url,
        'description': resource.description,
        'created_at': resource.created_at.isoformat() if resource.created_at else None,
    }

    # 文件夹：列出子内容
    if resource.is_folder:
        children = Resource.query.filter_by(parent_id=resource.id, status='approved').order_by(Resource.is_folder.desc(), Resource.created_at.desc()).all()
        data['children'] = [{
            'id': c.id,
            'name': c.original_name or c.name,
            'is_folder': c.is_folder,
            'file_size': c.file_size,
            'file_ext': c.file_ext,
            'file_url': c.file_url,
        } for c in children]

    return jsonify(data)


@api_bp.route('/share/<int:folder_id>/items', methods=['GET'])
def get_shared_folder_items(folder_id):
    token = request.args.get('token', '')

    # 验证 token 对应的共享资源
    shared = Resource.query.filter_by(share_token=token, status='approved').first()
    if not shared:
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    # 验证目标文件夹在共享范围内
    if shared.is_folder:
        # 检查 folder_id 是否是 shared 本身或其子孙
        current = Resource.query.get(folder_id)
        if not current or not current.is_folder:
            return jsonify({'error': 'not_found', 'message': '文件夹不存在'}), 404
        valid = (current.id == shared.id)
        if not valid:
            parent = current.parent
            while parent:
                if parent.id == shared.id:
                    valid = True
                    break
                parent = parent.parent
        if not valid:
            return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    else:
        # 共享的是文件，不支持子项浏览
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    children = Resource.query.filter_by(parent_id=folder_id, status='approved').order_by(Resource.is_folder.desc(), Resource.created_at.desc()).all()
    return jsonify({
        'name': current.original_name or current.name,
        'items': [{
            'id': c.id,
            'name': c.original_name or c.name,
            'is_folder': c.is_folder,
            'file_size': c.file_size,
            'file_ext': c.file_ext,
            'file_url': c.file_url,
            'description': c.description,
            'share_token': c.share_token,
            'created_at': c.created_at.isoformat() if c.created_at else None,
        } for c in children]
    })


@api_bp.route('/resources/<int:resource_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.status != 'approved':
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    comments = ResourceComment.query.filter_by(resource_id=resource_id).order_by(ResourceComment.created_at.desc()).all()
    return jsonify({'comments': [c.to_dict() for c in comments]})


@api_bp.route('/resources/<int:resource_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403
    user_id = int(identity.replace('user_', ''))

    resource = Resource.query.get(resource_id)
    if not resource or resource.status != 'approved':
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    data = request.get_json()
    content = (data.get('content') or '').strip()
    if not content:
        return jsonify({'error': 'validation', 'message': '评论内容不能为空'}), 400

    comment = ResourceComment(
        resource_id=resource_id,
        user_id=user_id,
        content=content,
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({'success': True, 'message': '评论成功', 'comment': comment.to_dict()}), 201


@api_bp.route('/resources/<int:resource_id>/file', methods=['GET'])
@jwt_required()
def proxy_resource_file(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.is_folder or resource.status != 'approved':
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    file_bytes = None
    content_type = 'application/octet-stream'
    if resource.file_url.startswith('/uploads/'):
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], resource.file_url.replace('/uploads/', ''))
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                file_bytes = f.read()
    else:
        import urllib.request as urlreq
        try:
            with urlreq.urlopen(resource.file_url, timeout=30) as resp:
                file_bytes = resp.read()
                ct = resp.headers.get('Content-Type', '')
                if ct: content_type = ct
        except Exception:
            pass

    if not file_bytes:
        return jsonify({'error': 'fetch_failed', 'message': '无法获取文件'}), 500

    from flask import Response
    from urllib.parse import quote
    return Response(file_bytes, content_type=content_type, headers={'Access-Control-Allow-Origin': '*'})


@api_bp.route('/resources/<int:resource_id>/preview', methods=['GET'])
@jwt_required()
def preview_resource(resource_id):
    identity = get_jwt_identity()
    if not identity.startswith('user_'):
        return jsonify({'error': 'forbidden', 'message': '无权访问'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.is_folder or resource.status != 'approved':
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    ext = (resource.file_ext or '').lower()

    if ext in IMAGE_EXTENSIONS:
        return jsonify({'type': 'image', 'url': resource.file_url})

    if ext in PDF_EXTENSIONS:
        return jsonify({'type': 'pdf', 'url': f'/api/resources/{resource_id}/file'})

    if ext in MARKDOWN_EXTENSIONS:
        content = _read_text_content(resource)
        return jsonify({'type': 'markdown', 'content': content or ''})

    if ext in TEXT_PREVIEW_EXTENSIONS:
        content = _read_text_content(resource)
        return jsonify({'type': 'text', 'content': content or '', 'language': ext})

    return jsonify({'type': 'unsupported', 'file_type': ext, 'file_name': resource.original_name})


def _read_text_content(resource):
    """读取文本文件内容（限 128MB）"""
    if not resource.file_size or resource.file_size > 128 * 1024 * 1024:
        return None
    try:
        if resource.file_url.startswith('/uploads/'):
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], resource.file_url.replace('/uploads/', ''))
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()[:500000]
        else:
            import urllib.request as urlreq
            with urlreq.urlopen(resource.file_url, timeout=15) as resp:
                return resp.read().decode('utf-8', errors='replace')[:500000]
    except Exception:
        pass
    return None


# ─── Resources: Admin API ───

@api_bp.route('/admin/resources', methods=['GET'])
@jwt_required()
def admin_get_resources():
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '').strip()
    is_folder = request.args.get('is_folder', '')
    parent_id = request.args.get('parent_id', type=int)

    query = Resource.query

    # 默认排除已删除的资源
    if status:
        query = query.filter_by(status=status)
    else:
        query = query.filter(Resource.status != 'deleted')

    # 有搜索关键词时，搜索所有文件夹；否则按 parent_id 过滤
    if search:
        query = query.filter(Resource.name.ilike(f'%{search}%'))
    elif parent_id is not None:
        query = query.filter_by(parent_id=parent_id)
    else:
        query = query.filter_by(parent_id=None)
    if is_folder == 'true':
        query = query.filter_by(is_folder=True)
    elif is_folder == 'false':
        query = query.filter_by(is_folder=False)

    query = query.order_by(Resource.is_folder.desc(), Resource.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # 状态计数
    counts = {
        'all': Resource.query.count(),
        'approved': Resource.query.filter_by(status='approved').count(),
        'pending': Resource.query.filter_by(status='pending').count(),
        'rejected': Resource.query.filter_by(status='rejected').count(),
        'deleted': Resource.query.filter_by(status='deleted').count(),
    }

    breadcrumb = []
    if parent_id:
        parent = Resource.query.get(parent_id)
        if parent:
            breadcrumb = _get_ancestor_chain(parent) + [{'id': parent.id, 'name': parent.name}]

    items = [r.to_dict() for r in pagination.items]

    # 搜索时为每个结果附加文件夹路径
    if search:
        for item, resource in zip(items, pagination.items):
            item['folder_path'] = '/'.join(a['name'] for a in _get_ancestor_chain(resource)) if resource.parent_id else ''

    return jsonify({
        'items': items,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': per_page,
        'pages': pagination.pages,
        'counts': counts,
        'breadcrumb': breadcrumb,
    })


@api_bp.route('/admin/resources/<int:resource_id>', methods=['PATCH'])
@jwt_required()
def admin_update_resource(resource_id):
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    data = request.get_json()
    if 'name' in data:
        old_name = resource.name
        new_name = data['name'].strip()
        if new_name != old_name:
            _log_action(resource.id, old_name, 'rename', admin.id, f'→ {new_name}')
        resource.name = new_name
    if 'tags' in data:
        resource.tags = data['tags'] if isinstance(data['tags'], list) else []
    if 'description' in data:
        resource.description = data['description'] if data['description'] else None

    db.session.commit()
    return jsonify({'success': True, 'message': '资源已更新', 'resource': resource.to_dict()})


@api_bp.route('/admin/resources/<int:resource_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_resource(resource_id):
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    # 软删除：标记为 deleted
    resource.status = 'deleted'
    resource.deleted_at = datetime.now(timezone.utc)

    # 如果是文件夹，递归软删除子项
    if resource.is_folder:
        _soft_delete_children(resource.id)

    _log_action(resource.id, resource.name, 'delete', admin.id)
    db.session.commit()
    return jsonify({'success': True, 'message': '已移入回收站'})


def _soft_delete_children(parent_id):
    children = Resource.query.filter_by(parent_id=parent_id).all()
    for child in children:
        child.status = 'deleted'
        child.deleted_at = datetime.now(timezone.utc)
        if child.is_folder:
            _soft_delete_children(child.id)


@api_bp.route('/admin/resources/trash', methods=['GET'])
@jwt_required()
def admin_get_trash():
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    query = Resource.query.filter_by(status='deleted').order_by(Resource.deleted_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [r.to_dict() for r in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': per_page,
        'pages': pagination.pages,
    })


@api_bp.route('/admin/resources/logs', methods=['GET'])
@jwt_required()
def admin_get_logs():
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    query = ResourceLog.query.order_by(ResourceLog.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [l.to_dict() for l in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': per_page,
        'pages': pagination.pages,
    })


@api_bp.route('/admin/resources/<int:resource_id>/restore', methods=['POST'])
@jwt_required()
def admin_restore_resource(resource_id):
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.status != 'deleted':
        return jsonify({'error': 'not_found', 'message': '资源不在回收站'}), 404

    resource.status = 'approved'
    resource.deleted_at = None

    # 如果是文件夹，递归恢复子项
    if resource.is_folder:
        _restore_children(resource.id)

    _log_action(resource.id, resource.name, 'restore', admin.id)
    db.session.commit()
    return jsonify({'success': True, 'message': '已恢复'})


def _restore_children(parent_id):
    children = Resource.query.filter_by(parent_id=parent_id, status='deleted').all()
    for child in children:
        child.status = 'approved'
        child.deleted_at = None
        if child.is_folder:
            _restore_children(child.id)


@api_bp.route('/admin/resources/<int:resource_id>/permanent', methods=['DELETE'])
@jwt_required()
def admin_permanent_delete(resource_id):
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    resource = Resource.query.get(resource_id)
    if not resource or resource.status != 'deleted':
        return jsonify({'error': 'not_found', 'message': '资源不在回收站'}), 404

    # 删除实际文件
    if resource.oss_key:
        try:
            oss_service.delete_file(resource.oss_key)
        except Exception:
            pass
    elif resource.file_url and resource.file_url.startswith('/uploads/'):
        try:
            local_path = os.path.join(current_app.config['UPLOAD_FOLDER'], resource.file_url.replace('/uploads/', ''))
            if os.path.exists(local_path):
                os.remove(local_path)
        except Exception:
            pass

    # 递归永久删除子项
    if resource.is_folder:
        _permanent_delete_children(resource.id)

    db.session.delete(resource)
    db.session.commit()
    return jsonify({'success': True, 'message': '已永久删除'})


def _permanent_delete_children(parent_id):
    children = Resource.query.filter_by(parent_id=parent_id).all()
    for child in children:
        if child.oss_key:
            try:
                oss_service.delete_file(child.oss_key)
            except Exception:
                pass
        elif child.file_url and child.file_url.startswith('/uploads/'):
            try:
                local_path = os.path.join(current_app.config['UPLOAD_FOLDER'], child.file_url.replace('/uploads/', ''))
                if os.path.exists(local_path):
                    os.remove(local_path)
            except Exception:
                pass
        if child.is_folder:
            _permanent_delete_children(child.id)
        db.session.delete(child)


@api_bp.route('/admin/resources/folders', methods=['GET'])
@jwt_required()
def admin_get_folders():
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    folders = Resource.query.filter_by(is_folder=True).order_by(Resource.name).all()

    # 构建 id→folder 映射，用于快速查找祖先路径
    folder_map = {f.id: f for f in folders}

    def build_path(fid):
        """构建文件夹完整路径，如 '根目录 / 子文件夹 / 深层文件夹'"""
        parts = []
        current = folder_map.get(fid)
        while current:
            parts.insert(0, current.name)
            current = folder_map.get(current.parent_id)
        return ' / '.join(parts) if parts else ''

    result = [{'id': f.id, 'name': f.name, 'parent_id': f.parent_id, 'path': build_path(f.id)} for f in folders]
    return jsonify({'folders': result})


@api_bp.route('/admin/resources/<int:resource_id>/move', methods=['POST'])
@jwt_required()
def admin_move_resource(resource_id):
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    data = request.get_json()
    new_parent_id = data.get('new_parent_id')

    # 不能移动到自身
    if new_parent_id == resource_id:
        return jsonify({'error': 'validation', 'message': '不能移动到自身'}), 400

    # 验证目标文件夹存在且是文件夹
    if new_parent_id:
        target = Resource.query.get(new_parent_id)
        if not target or not target.is_folder:
            return jsonify({'error': 'validation', 'message': '目标文件夹不存在'}), 400

    old_parent = resource.parent_id
    resource.parent_id = new_parent_id if new_parent_id else None
    _log_action(resource.id, resource.name, 'move', admin.id, f'从 {old_parent} → {new_parent_id}')
    db.session.commit()
    return jsonify({'success': True, 'message': '移动成功', 'resource': resource.to_dict()})


@api_bp.route('/admin/resources/<int:resource_id>/status', methods=['PATCH'])
@jwt_required()
def admin_update_resource_status(resource_id):
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    data = request.get_json()
    new_status = data.get('status')
    if new_status not in ('approved', 'pending', 'rejected'):
        return jsonify({'error': 'validation', 'message': '无效的状态值'}), 400

    resource.status = new_status
    db.session.commit()
    return jsonify({'success': True, 'message': '状态已更新', 'resource': resource.to_dict()})


@api_bp.route('/admin/resources/batch', methods=['POST'])
@jwt_required()
def admin_batch_resources():
    admin = _require_admin()
    if not admin:
        return jsonify({'error': 'unauthorized', 'message': '需要管理员权限'}), 403

    data = request.get_json()
    ids = data.get('ids', [])
    action = data.get('action')
    new_parent_id = data.get('new_parent_id')

    if not ids or not action:
        return jsonify({'error': 'validation', 'message': '缺少 ids 或 action'}), 400

    updated = 0
    for rid in ids:
        resource = Resource.query.get(rid)
        if not resource:
            continue

        if action == 'delete':
            if resource.is_folder and Resource.query.filter_by(parent_id=resource.id).count() > 0:
                continue
            if resource.oss_key:
                try:
                    oss_service.delete_file(resource.oss_key)
                except Exception:
                    pass
            elif resource.file_url and resource.file_url.startswith('/uploads/'):
                try:
                    local_path = os.path.join(current_app.config['UPLOAD_FOLDER'], resource.file_url.replace('/uploads/', ''))
                    if os.path.exists(local_path):
                        os.remove(local_path)
                except Exception:
                    pass
            db.session.delete(resource)
            updated += 1
        elif action == 'approve':
            resource.status = 'approved'
            updated += 1
        elif action == 'reject':
            resource.status = 'rejected'
            updated += 1
        elif action == 'move' and new_parent_id is not None:
            if rid != new_parent_id:
                resource.parent_id = new_parent_id if new_parent_id else None
                updated += 1

    db.session.commit()
    return jsonify({'success': True, 'message': f'已处理 {updated} 项', 'updated': updated})
