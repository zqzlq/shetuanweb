import oss2
from flask import current_app

_bucket = None


def get_bucket():
    global _bucket
    if _bucket is not None:
        return _bucket

    cfg = current_app.config
    ak = cfg.get('ALIYUN_ACCESS_KEY_ID', '')
    sk = cfg.get('ALIYUN_ACCESS_KEY_SECRET', '')
    endpoint = cfg.get('ALIYUN_OSS_ENDPOINT', '')
    bucket_name = cfg.get('ALIYUN_OSS_BUCKET_NAME', '')

    if not all([ak, sk, endpoint, bucket_name]):
        return None

    try:
        auth = oss2.Auth(ak, sk)
        _bucket = oss2.Bucket(auth, endpoint, bucket_name)
        return _bucket
    except Exception:
        return None


def _get_public_url(key):
    cfg = current_app.config
    cdn_url = cfg.get('ALIYUN_OSS_CDN_URL', '')
    if cdn_url:
        return f"{cdn_url.rstrip('/')}/{key}"
    bucket_name = cfg.get('ALIYUN_OSS_BUCKET_NAME', '')
    endpoint = cfg.get('ALIYUN_OSS_ENDPOINT', '')
    return f"https://{bucket_name}.{endpoint}/{key}"


def upload_file(key, data):
    bucket = get_bucket()
    if not bucket:
        return None
    try:
        bucket.put_object(key, data)
        return _get_public_url(key)
    except Exception:
        return None


def delete_file(key):
    bucket = get_bucket()
    if not bucket:
        return False
    try:
        bucket.delete_object(key)
        return True
    except Exception:
        return False
