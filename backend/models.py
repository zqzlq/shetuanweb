from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class SiteConfig(db.Model):
    __tablename__ = 'site_config'

    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(50), unique=True, nullable=False)
    config_value = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'key': self.config_key,
            'value': self.config_value,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title,
            'content': self.content,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    grade_major = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    group_id = db.Column(db.String(50), nullable=False)
    group_name = db.Column(db.String(100), nullable=False)
    github_url = db.Column(db.String(255), nullable=True)
    portfolio_url = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Text, nullable=True)
    motivation = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(64), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    session = db.Column(db.String(50), nullable=True)
    admin_note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    processed_at = db.Column(db.DateTime, nullable=True)
    last_email_type = db.Column(db.String(50), nullable=True)
    last_email_sent = db.Column(db.Boolean, default=False)
    last_email_error = db.Column(db.String(500), nullable=True)
    last_email_sent_at = db.Column(db.DateTime, nullable=True)
    feishu_delivery_mode = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'student_id': self.student_id,
            'grade_major': self.grade_major,
            'phone': self.phone,
            'email': self.email,
            'group_id': self.group_id,
            'group_name': self.group_name,
            'github_url': self.github_url,
            'portfolio_url': self.portfolio_url,
            'experience': self.experience,
            'motivation': self.motivation,
            'ip_address': self.ip_address,
            'status': self.status,
            'session': self.session,
            'admin_note': self.admin_note,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'last_email_type': self.last_email_type,
            'last_email_sent': self.last_email_sent,
            'last_email_error': self.last_email_error,
            'last_email_sent_at': self.last_email_sent_at.isoformat() if self.last_email_sent_at else None,
            'feishu_delivery_mode': self.feishu_delivery_mode,
        }


class AdminUser(db.Model):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class MemberUser(db.Model):
    __tablename__ = 'member_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    avatar = db.Column(db.String(500), nullable=True)
    group_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    social_links = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'student_id': self.student_id,
            'phone': self.phone,
            'avatar': self.avatar,
            'group': self.group_name or '',
            'bio': self.bio,
            'social_links': self.social_links,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class UserSubmission(db.Model):
    __tablename__ = 'user_submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('member_users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'award' or 'project'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('MemberUser', backref='submissions')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'status': self.status,
            'data': self.data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    is_folder = db.Column(db.Boolean, default=False, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    tags = db.Column(db.JSON, nullable=True)
    description = db.Column(db.Text, nullable=True)

    # 文件专属字段（文件夹为 null）
    file_url = db.Column(db.String(500), nullable=True)
    oss_key = db.Column(db.String(500), nullable=True)
    original_name = db.Column(db.String(255), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)
    mime_type = db.Column(db.String(100), nullable=True)
    file_ext = db.Column(db.String(20), nullable=True)

    # 元数据
    uploader_id = db.Column(db.Integer, db.ForeignKey('member_users.id'), nullable=True)
    status = db.Column(db.String(20), default='approved')
    download_count = db.Column(db.Integer, default=0)
    share_token = db.Column(db.String(64), nullable=True, unique=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    parent = db.relationship('Resource', remote_side=[id], backref='children')
    uploader = db.relationship('MemberUser', backref='resources')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_folder': self.is_folder,
            'parent_id': self.parent_id,
            'category': self.category,
            'tags': self.tags or [],
            'description': self.description,
            'file_url': self.file_url,
            'original_name': self.original_name,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'file_ext': self.file_ext,
            'uploader_id': self.uploader_id,
            'uploader_name': self.uploader.name if self.uploader else None,
            'status': self.status,
            'download_count': self.download_count,
            'children_count': len(self.children) if self.is_folder else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class ResourceVersion(db.Model):
    __tablename__ = 'resource_versions'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    version = db.Column(db.Integer, nullable=False, default=1)
    file_url = db.Column(db.String(500), nullable=False)
    oss_key = db.Column(db.String(500), nullable=True)
    original_name = db.Column(db.String(255), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)
    file_ext = db.Column(db.String(20), nullable=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey('member_users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    resource = db.relationship('Resource', backref='versions')
    uploader = db.relationship('MemberUser', backref='resource_versions')

    def to_dict(self):
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'version': self.version,
            'file_url': self.file_url,
            'original_name': self.original_name,
            'file_size': self.file_size,
            'file_ext': self.file_ext,
            'uploader_id': self.uploader_id,
            'uploader_name': self.uploader.name if self.uploader else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ResourceLog(db.Model):
    __tablename__ = 'resource_logs'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, nullable=True)
    resource_name = db.Column(db.String(255), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # upload, download, delete, restore, rename, move
    detail = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('member_users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('MemberUser', backref='resource_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'action': self.action,
            'detail': self.detail,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ResourceComment(db.Model):
    __tablename__ = 'resource_comments'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('member_users.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    resource = db.relationship('Resource', backref='comments')
    user = db.relationship('MemberUser', backref='resource_comments')

    def to_dict(self):
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'user_avatar': self.user.avatar if self.user else None,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='匿名用户')
    email = db.Column(db.String(120), nullable=False, default='')
    phone = db.Column(db.String(30), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(64), nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), nullable=False, default='unread')
    admin_note = db.Column(db.Text, nullable=True)
    reply = db.Column(db.Text, nullable=True)
    replied_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    read_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'ip_address': self.ip_address,
            'is_anonymous': self.is_anonymous,
            'status': self.status,
            'admin_note': self.admin_note,
            'reply': self.reply,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None,
        }
