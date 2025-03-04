from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

# Tabela de associação entre Role e Permission
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', name='fk_role_permissions_role')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id', name='fk_role_permissions_permission'))
)

# Tabela de associação entre Article e Tag
article_tags = db.Table('article_tags',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id', name='fk_article_tags_article')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', name='fk_article_tags_tag'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', name='fk_user_role'))
    articles = db.relationship('Article', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name):
        if not self.role:
            return False
        return any(p.name == permission_name for p in self.role.permissions)

    def has_any_permission(self, permission_names):
        if not self.role:
            return False
        return any(p.name in permission_names for p in self.role.permissions)

    def has_all_permissions(self, permission_names):
        if not self.role:
            return False
        user_permissions = {p.name for p in self.role.permissions}
        return all(name in user_permissions for name in permission_names)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(200))
    permissions = db.relationship('Permission', secondary=role_permissions, lazy='subquery',
        backref=db.backref('roles', lazy=True))
    users = db.relationship('User', backref='role', lazy=True)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(200))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    articles = db.relationship('Article', backref='category_rel', lazy=True)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', name='fk_article_category'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_article_user'), nullable=False)
    tags = db.relationship('Tag', secondary=article_tags, lazy='subquery',
        backref=db.backref('articles', lazy=True))

    def __repr__(self):
        return f'<Article {self.title}>' 