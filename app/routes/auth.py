from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not username or not email or not password:
            flash('Please fill in all required fields.', 'danger')
            return render_template('auth/register.html')

        if len(username) < 3:
            flash('Username must be at least 3 characters long.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(username=username).first():
            flash('That username is already taken. Please choose another.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'danger')
            return render_template('auth/register.html')

        # Create user
        user = User(
            username=username,
            email=email,
            full_name=full_name if full_name else username
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Account created successfully! Welcome to BlogNest.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        login_identifier = request.form.get('login_identifier', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not login_identifier or not password:
            flash('Please enter both your username/email and password.', 'danger')
            return render_template('auth/login.html')

        # Allow login via username or email
        user = User.query.filter(
            (User.username == login_identifier) | (User.email == login_identifier.lower())
        ).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.display_name}!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username/email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        bio = request.form.get('bio', '').strip()
        avatar_url = request.form.get('avatar_url', '').strip()

        current_user.full_name = full_name
        current_user.bio = bio
        current_user.avatar_url = avatar_url if avatar_url else None

        db.session.commit()
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html')
