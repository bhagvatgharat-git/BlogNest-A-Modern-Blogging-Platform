import re
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(400), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def display_name(self):
        return self.full_name if self.full_name else self.username

    @property
    def initials(self):
        name = self.display_name.strip()
        if not name:
            return 'U'
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        return name[0:2].upper()

    @property
    def published_posts_count(self):
        return self.posts.filter_by(is_published=True).count()

    @property
    def drafts_count(self):
        return self.posts.filter_by(is_published=False).count()

    @property
    def total_views(self):
        return sum(post.views_count for post in self.posts.all())

    @property
    def total_comments_received(self):
        return sum(post.comments.count() for post in self.posts.all())

    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    color_code = db.Column(db.String(20), default='#0284c7')

    posts = db.relationship('Post', backref='category', lazy='dynamic')

    @property
    def published_count(self):
        return self.posts.filter_by(is_published=True).count()

    def __repr__(self):
        return f'<Category {self.name}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220), nullable=False)
    slug = db.Column(db.String(260), unique=True, nullable=False, index=True)
    summary = db.Column(db.String(400), nullable=True)
    content = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(400), nullable=True)
    is_published = db.Column(db.Boolean, default=True, index=True)
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    comments = db.relationship(
        'Comment', 
        backref='post', 
        lazy='dynamic', 
        cascade='all, delete-orphan',
        order_by='Comment.created_at.desc()'
    )

    @property
    def reading_time_minutes(self):
        if not self.content:
            return 1
        word_count = len(re.findall(r'\w+', self.content))
        return max(1, round(word_count / 200))

    @property
    def comments_count(self):
        return self.comments.count()

    @staticmethod
    def generate_slug(title):
        clean = re.sub(r'[^\w\s-]', '', title.lower()).strip()
        slug = re.sub(r'[-\s]+', '-', clean)
        # Check uniqueness
        unique_slug = slug
        counter = 1
        while Post.query.filter_by(slug=unique_slug).first():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug

    def __repr__(self):
        return f'<Post {self.title}>'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.id} on Post {self.post_id}>'
