import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import config
from models import db, AdminUser, SiteConfig, Page
from defaults import DEFAULT_SITE_CONFIG, DEFAULT_PAGES
from routes.api import api_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    JWTManager(app)

    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()
        _migrate_columns(app)
        _seed_defaults()
        _load_mail_config(app)

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok', 'message': 'Xingyu CMS API is running'})

    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'not_found', 'message': '资源不存在'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'server_error', 'message': '服务器内部错误'}), 500

    return app


def _seed_defaults():
    try:
        if not AdminUser.query.first():
            admin = AdminUser(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)

        if not SiteConfig.query.first():
            for key, value in DEFAULT_SITE_CONFIG.items():
                db.session.add(SiteConfig(config_key=key, config_value=value))

        if not Page.query.first():
            for slug, data in DEFAULT_PAGES.items():
                db.session.add(Page(slug=slug, title=data['title'], content=data['content']))

        db.session.commit()
    except Exception:
        db.session.rollback()


def _migrate_columns(app):
    """Add missing columns to existing tables (SQLite ALTER TABLE)."""
    new_columns = [
        ('applications', 'processed_at', 'DATETIME'),
        ('applications', 'last_email_type', 'VARCHAR(50)'),
        ('applications', 'last_email_sent', 'BOOLEAN DEFAULT 0'),
        ('applications', 'last_email_error', 'VARCHAR(500)'),
        ('applications', 'last_email_sent_at', 'DATETIME'),
        ('applications', 'feishu_delivery_mode', 'VARCHAR(20)'),
    ]
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                for table, col, col_type in new_columns:
                    try:
                        conn.execute(db.text(f'ALTER TABLE {table} ADD COLUMN {col} {col_type}'))
                        conn.commit()
                    except Exception:
                        pass  # column already exists
        except Exception:
            pass


def _load_mail_config(app):
    try:
        system_cfg = SiteConfig.query.filter_by(config_key='system').first()
        cfg = system_cfg.config_value if system_cfg and isinstance(system_cfg.config_value, dict) else {}

        # 环境变量覆盖（敏感信息优先从环境变量读取）
        import os
        def env_or(key, fallback):
            return os.environ.get(key) or fallback

        # 邮件配置
        app.config['MAIL_ENABLED'] = cfg.get('mailEnabled', False) or os.environ.get('MAIL_ENABLED', '').lower() in ('1', 'true', 'yes')
        app.config['SMTP_HOST'] = env_or('SMTP_HOST', cfg.get('smtpHost', ''))
        app.config['SMTP_PORT'] = int(env_or('SMTP_PORT', cfg.get('smtpPort', 465)))
        app.config['SMTP_USERNAME'] = env_or('SMTP_USERNAME', cfg.get('smtpUsername', ''))
        app.config['SMTP_PASSWORD'] = env_or('SMTP_PASSWORD', cfg.get('smtpPassword', ''))
        app.config['MAIL_FROM_EMAIL'] = env_or('MAIL_FROM_EMAIL', cfg.get('mailFromEmail', ''))
        app.config['MAIL_FROM_NAME'] = cfg.get('mailFromName', '星雨作坊')
        app.config['SMTP_USE_SSL'] = cfg.get('smtpUseSsl', True)
        app.config['SMTP_USE_TLS'] = cfg.get('smtpUseTls', False)
        # 飞书配置
        app.config['FEISHU_APP_ENABLED'] = cfg.get('feishuMode') == 'app' or os.environ.get('FEISHU_APP_ENABLED', '').lower() in ('1', 'true', 'yes')
        app.config['FEISHU_APP_ID'] = env_or('FEISHU_APP_ID', cfg.get('feishuAppId', ''))
        app.config['FEISHU_APP_SECRET'] = env_or('FEISHU_APP_SECRET', cfg.get('feishuAppSecret', ''))
        app.config['FEISHU_APP_CHAT_ID'] = env_or('FEISHU_APP_CHAT_ID', cfg.get('feishuAppChatId', ''))
        app.config['FEISHU_APP_VERIFICATION_TOKEN'] = env_or('FEISHU_APP_VERIFICATION_TOKEN', cfg.get('feishuAppVerificationToken', ''))
        app.config['FEISHU_APP_ENCRYPT_KEY'] = env_or('FEISHU_APP_ENCRYPT_KEY', cfg.get('feishuAppEncryptKey', ''))
        app.config['FEISHU_WEBHOOK_URL'] = env_or('FEISHU_WEBHOOK_URL', cfg.get('feishuWebhookUrl', ''))
    except Exception:
        pass


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['APP_HOST'],
        port=app.config['APP_PORT'],
        debug=app.config['DEBUG'],
    )
