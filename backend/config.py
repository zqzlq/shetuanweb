import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _get_bool(name, default=False):
    val = os.environ.get(name, '')
    if not val:
        return default
    return val.lower() in ('1', 'true', 'yes', 'on')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'xingyu-studio-secret-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "xingyu_cms.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'xingyu-jwt-secret-2026')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    CORS_ORIGINS = os.environ.get(
        'CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000'
    ).split(',')

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 10 * 1024 * 1024))

    APPLICATION_RATE_LIMIT_MINUTES = int(os.environ.get('APPLICATION_RATE_LIMIT_MINUTES', 10))

    # 阿里云 OSS（配置后自动上传到 OSS，未配置则使用本地存储）
    ALIYUN_ACCESS_KEY_ID = os.environ.get('ALIYUN_ACCESS_KEY_ID', '')
    ALIYUN_ACCESS_KEY_SECRET = os.environ.get('ALIYUN_ACCESS_KEY_SECRET', '')
    ALIYUN_OSS_ENDPOINT = os.environ.get('ALIYUN_OSS_ENDPOINT', '')
    ALIYUN_OSS_BUCKET_NAME = os.environ.get('ALIYUN_OSS_BUCKET_NAME', '')
    ALIYUN_OSS_CDN_URL = os.environ.get('ALIYUN_OSS_CDN_URL', '')

    APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.environ.get('APP_PORT', 5000))
    APP_DEBUG = _get_bool('APP_DEBUG', True)


class DevelopmentConfig(Config):
    DEBUG = Config.APP_DEBUG


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
