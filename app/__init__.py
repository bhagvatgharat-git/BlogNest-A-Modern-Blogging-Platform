import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # User loader for Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.blog import blog_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Context processors for global template access
    from app.models import Category
    @app.context_processor
    def inject_global_data():
        try:
            categories = Category.query.order_by(Category.name.asc()).all()
        except Exception:
            categories = []
        return {
            'global_categories': categories,
            'app_name': 'BlogNest'
        }

    # Custom Jinja Template Filters
    @app.template_filter('reading_time')
    def reading_time_filter(content):
        if not content:
            return 1
        word_count = len(content.split())
        minutes = max(1, round(word_count / 200))
        return minutes

    @app.template_filter('format_date')
    def format_date_filter(date_val, fmt='%b %d, %Y'):
        if not date_val:
            return ''
        return date_val.strftime(fmt)

    # Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    return app
