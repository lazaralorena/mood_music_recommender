from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect

from models import db, User
from api.auth_routes import auth_bp
from api.music_routes import music_bp
from api.main_routes import main_bp
from config.config import config

def create_app(config_name: str = 'default') -> Flask:
    """Create and configure the Flask application.
    
    Args:
        config_name: The configuration to use (default, development, production, testing)
        
    Returns:
        Flask: The configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    CSRFProtect(app)
    db.init_app(app)
    
    # Setup rate limiting
    Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[app.config['RATELIMIT_DEFAULT']]
    )
    
    # Setup login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(music_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run() 