from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Render the home page or redirect to login if not authenticated."""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('index.html') 