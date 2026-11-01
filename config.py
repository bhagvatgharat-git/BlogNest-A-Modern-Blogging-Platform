import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'blognest-dev-secret-key-3984729183749')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f"sqlite:///{BASE_DIR / 'instance' / 'blognest.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 6
    COMMENTS_PER_POST = 20

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
