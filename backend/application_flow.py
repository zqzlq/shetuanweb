import json
import smtplib
import time
from datetime import datetime
from email.message import EmailMessage
from email.mime.image import MIMEImage
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError

from flask import current_app

from models import SiteConfig


def get_feishu_system_config():
    try:
        system_config = SiteConfig.query.filter_by(config_key='system').first()
        if system_config and isinstance(system_config.config_value, dict):
            return system_config.config_value
    except Exception:
        return {}
    return {}


def get_feishu_webhook_url():
    webhook_url = (get_feishu_system_config().get('feishuWebhookUrl') or '').strip()
    if not webhook_url:
        webhook_url = (current_app.config.get('FEISHU_WEBHOOK_URL') or '').strip()
    return webhook_url


def get_feishu_http_settings():
    try:
        timeout = float(current_app.config.get('FEISHU_HTTP_TIMEOUT') or 8)
    except (TypeError, ValueError):
        timeout = 8
    try:
        retries = int(current_app.config.get('FEISHU_HTTP_RETRIES') or 2)
    except (TypeError, ValueError):
        retries = 2
    try:
        backoff = float(current_app.config.get('FEISHU_HTTP_RETRY_BACKOFF') or 0.6)
    except (TypeError, ValueError):
        backoff = 0.6
    return max(timeout, 1), max(retries, 0), max(backoff, 0)


def urlopen_with_retry(req):
    timeout, retries, backoff = get_feishu_http_settings()
    last_error = None
    for attempt in range(retries + 1):
        try:
            return urllib_request.urlopen(req, timeout=timeout)
        except (HTTPError, URLError, TimeoutError) as error:
            last_error = error
            if isinstance(error, HTTPError) and getattr(error, 'code', 0) and error.code < 500:
                raise
            if attempt >= retries:
                raise
            time.sleep(backoff * (2 ** attempt))
    raise last_error


def send_feishu_webhook_payload(payload):
    webhook_url = get_feishu_webhook_url()
    if not webhook_url:
        return False, 'FEISHU_WEBHOOK_URL 未配置'

    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib_request.Request(
        webhook_url,
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urlopen_with_retry(req) as response:
            resp_body = json.loads(response.read().decode('utf-8') or '{}')
            if resp_body.get('StatusCode') == 0:
                return True, ''
            return False, resp_body.get('StatusMessage', '飞书通知失败')
    except (HTTPError, URLError, TimeoutError) as error:
        return False, str(error)


def build_application_card(application, title, status_label, template='blue'):
    elements = [
        {'tag': 'markdown', 'content': f'**当前状态**：{status_label}'},
        {'tag': 'markdown', 'content': f'**报名方向**：{application.group_name}'},
        {'tag': 'markdown', 'content': f'**姓名**：{application.name}\n**学号**：{application.student_id}'},
        {'tag': 'markdown', 'content': f'**专业年级**：{application.grade_major}\n**手机号**：{application.phone}'},
        {'tag': 'markdown', 'content': f'**邮箱**：{application.email}\n**GitHub**：{application.github_url or "未填写"}'},
        {'tag': 'markdown', 'content': f'**作品集**：{application.portfolio_url or "未填写"}'},
        {'tag': 'markdown', 'content': f'**相关经历**：\n{application.experience or "未填写"}'},
        {'tag': 'markdown', 'content': f'**报名说明**：\n{application.motivation}'}
    ]

    if application.admin_note:
        elements.append({'tag': 'markdown', 'content': f'**后台备注**：\n{application.admin_note}'})

    if application.last_email_type:
        email_status = '已发送' if application.last_email_sent else f'发送失败：{application.last_email_error or "未知错误"}'
        elements.append({'tag': 'markdown', 'content': f'**最近邮件**：{application.last_email_type} · {email_status}'})

    elements.append({
        'tag': 'note',
        'elements': [
            {'tag': 'plain_text', 'content': f'提交时间：{application.created_at.strftime("%Y-%m-%d %H:%M:%S")}'}
        ]
    })

    return {
        'config': {'wide_screen_mode': True},
        'header': {
            'title': {'tag': 'plain_text', 'content': title},
            'template': template
        },
        'elements': elements
    }


def get_status_label(application):
    status = application.status
    if status == 'pending':
        return '待处理'
    if status == 'reviewing':
        return '审核中'
    if status == 'approved':
        return '已通过'
    if status == 'rejected':
        return '已拒绝'
    if status == 'archived':
        return '已归档'
    return status


def send_pending_application_card(application):
    application.feishu_delivery_mode = 'webhook'
    card = build_application_card(
        application,
        f'新的报名申请 - {application.name}',
        '待处理',
        template='blue'
    )
    return send_feishu_webhook_payload({
        'msg_type': 'interactive',
        'card': card
    })


def send_status_update_card(application):
    status_label = get_status_label(application)
    application.feishu_delivery_mode = 'webhook'
    card = build_application_card(
        application,
        f'报名处理更新 - {application.name}',
        status_label,
        template='turquoise'
    )
    return send_feishu_webhook_payload({
        'msg_type': 'interactive',
        'card': card
    })


def send_contact_notification(contact_msg):
    elements = [
        {'tag': 'markdown', 'content': f'**姓名**：{contact_msg.name}\n**邮箱**：{contact_msg.email}'},
        {'tag': 'markdown', 'content': f'**电话**：{contact_msg.phone or "未填写"}'},
        {'tag': 'markdown', 'content': f'**主题**：{contact_msg.subject}'},
        {'tag': 'markdown', 'content': f'**留言内容**：\n{contact_msg.message}'},
        {
            'tag': 'note',
            'elements': [
                {'tag': 'plain_text', 'content': f'提交时间：{contact_msg.created_at.strftime("%Y-%m-%d %H:%M:%S")}'}
            ]
        }
    ]

    card = {
        'config': {'wide_screen_mode': True},
        'header': {
            'title': {'tag': 'plain_text', 'content': f'新的留言 - {contact_msg.name}'},
            'template': 'orange'
        },
        'elements': elements
    }

    return send_feishu_webhook_payload({
        'msg_type': 'interactive',
        'card': card
    })


# ─── Email ───

def _escape_html(value):
    text = '' if value is None else str(value)
    return (
        text.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;')
    )


def _download_image(url):
    """下载图片返回 (bytes, mime_type)，失败返回 None"""
    if not url:
        return None
    try:
        req = urllib_request.Request(url, headers={'User-Agent': 'XingyuCMS/2.0'})
        with urllib_request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            mime = resp.headers.get('Content-Type', 'image/png')
            return data, mime
    except Exception:
        return None


def get_site_logo_url():
    """从系统配置读取站点 logo URL"""
    try:
        system_cfg = SiteConfig.query.filter_by(config_key='system').first()
        if system_cfg and isinstance(system_cfg.config_value, dict):
            return (system_cfg.config_value.get('siteIcon') or '').strip()
    except Exception:
        pass
    return ''


def send_email(subject, to_email, text_content, html_content=None, inline_images=None):
    if not current_app.config.get('MAIL_ENABLED'):
        return False, '邮件发送未启用'

    smtp_host = (current_app.config.get('SMTP_HOST') or '').strip()
    smtp_username = (current_app.config.get('SMTP_USERNAME') or '').strip()
    smtp_password = (current_app.config.get('SMTP_PASSWORD') or '').strip()
    from_email = (current_app.config.get('MAIL_FROM_EMAIL') or '').strip()

    if not smtp_host or not from_email or not to_email:
        return False, '邮件配置不完整'

    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = f'{current_app.config.get("MAIL_FROM_NAME", "星雨作坊")} <{from_email}>'
    message['To'] = to_email
    message.set_content(text_content)

    # 构建 HTML 并添加内嵌图片作为相关附件
    if html_content:
        # 先设置 HTML 内容
        message.add_alternative(html_content, subtype='html')

    # 添加内嵌图片（inline attachments with Content-ID）
    if inline_images:
        for cid, (img_bytes, mime_type) in inline_images.items():
            maintype, subtype = mime_type.split('/', 1) if '/' in mime_type else ('image', 'png')
            img = MIMEImage(img_bytes, _subtype=subtype)
            img.add_header('Content-ID', f'<{cid}>')
            img.add_header('Content-Disposition', 'inline', filename=f'{cid}.{subtype}')
            message.attach(img)

    smtp_port = current_app.config.get('SMTP_PORT') or 587
    smtp_use_ssl = current_app.config.get('SMTP_USE_SSL')
    smtp_use_tls = current_app.config.get('SMTP_USE_TLS')

    try:
        if smtp_use_ssl:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10) as server:
                if smtp_username:
                    server.login(smtp_username, smtp_password)
                server.send_message(message)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                if smtp_use_tls:
                    server.starttls()
                if smtp_username:
                    server.login(smtp_username, smtp_password)
                server.send_message(message)
        return True, ''
    except Exception as error:
        return False, str(error)


def build_result_email(application, group_link_override=None, qr_code_url=None):
    group_name = application.group_name or '社团'
    name = application.name

    # 读取站点 logo
    logo_url = get_site_logo_url()

    # 优先使用传入的链接，否则读取系统配置
    group_link = group_link_override or ''
    if not group_link:
        try:
            system_cfg = SiteConfig.query.filter_by(config_key='system').first()
            if system_cfg and isinstance(system_cfg.config_value, dict):
                group_link = (system_cfg.config_value.get('groupChatInviteLink') or '').strip()
        except Exception:
            pass

    # 邮件底部 logo
    logo_html = '<p><img src="cid:logo" alt="星雨作坊" style="max-width:120px;margin-top:20px;" /></p>' if logo_url else ''

    if application.status == 'approved':
        qr_html = f'<p><img src="cid:qrcode" alt="考核群二维码" style="max-width:280px;border-radius:8px;" /></p>' if qr_code_url else ''
        group_link_html = f'<p>请点击以下链接或扫描二维码加入考核群：<br><a href="{_escape_html(group_link)}">{_escape_html(group_link)}</a></p>{qr_html}' if group_link else '<p>请留意后续通知加入考核群。</p>'
        group_link_text = f'\n请通过以下链接加入考核群：{group_link}' if group_link else '\n请留意后续通知加入考核群。'
        text_content = f'''{name} 同学，你好：

感谢你报名 {group_name}。
你的报名申请已通过，请加入考核群。{group_link_text}

星雨作坊'''
        html_content = f'''<div style="max-width:600px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
<p>{_escape_html(name)} 同学，你好：</p>
<p>感谢你报名 <strong>{_escape_html(group_name)}</strong>。</p>
<p>你的报名申请已通过，请加入考核群。</p>
{group_link_html}
{logo_html}
</div>'''
        return '星雨作坊报名结果通知', text_content, html_content, 'result_approved'

    text_content = f'''{name} 同学，你好：

感谢你报名 {group_name}。
很遗憾，本次未能通过筛选，但仍感谢你的关注与投入。
欢迎后续继续关注星雨作坊的活动与招新信息。

星雨作坊'''
    html_content = f'''<div style="max-width:600px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
<p>{_escape_html(name)} 同学，你好：</p>
<p>感谢你报名 <strong>{_escape_html(group_name)}</strong>。</p>
<p>很遗憾，本次未能通过筛选，但仍感谢你的关注与投入。</p>
<p>欢迎后续继续关注星雨作坊的活动与招新信息。</p>
{logo_html}
</div>'''
    return '星雨作坊报名结果通知', text_content, html_content, 'result_rejected'


def send_status_email(application, mail_kind, group_link=None, qr_code_url=None):
    subject, content, html_content, email_type = build_result_email(application, group_link, qr_code_url)

    # 准备内嵌图片
    inline_images = {}
    logo_url = get_site_logo_url()
    if logo_url:
        img_data = _download_image(logo_url)
        if img_data:
            inline_images['logo'] = img_data
    if qr_code_url:
        img_data = _download_image(qr_code_url)
        if img_data:
            inline_images['qrcode'] = img_data

    sent, error = send_email(subject, application.email, content, html_content, inline_images)
    application.last_email_type = email_type
    application.last_email_sent = sent
    application.last_email_error = error or None
    application.last_email_sent_at = datetime.utcnow() if sent else None
    return sent, error


def send_status_email(application, mail_kind, group_link=None, qr_code_url=None):
    subject, content, html_content, email_type = build_result_email(application, group_link, qr_code_url)
    sent, error = send_email(subject, application.email, content, html_content)
    application.last_email_type = email_type
    application.last_email_sent = sent
    application.last_email_error = error or None
    application.last_email_sent_at = datetime.utcnow() if sent else None
    return sent, error
