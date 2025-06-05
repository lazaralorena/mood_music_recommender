from flask import Blueprint, request, jsonify, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([username, email, password]):
            flash('All fields are required')
            return redirect(url_for('auth.register'))
            
        message, success = AuthService.register_user(username, email, password)
        flash(message)
        
        if success:
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.register'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not all([username, password]):
            flash('All fields are required')
            return redirect(url_for('auth.login'))
            
        user, message = AuthService.authenticate_user(username, password)
        flash(message)
        
        if user:
            login_user(user)
            return redirect(url_for('main.home'))
        return redirect(url_for('auth.login'))
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('main.home')) 