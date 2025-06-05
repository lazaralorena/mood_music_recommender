import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    
    SECRET_KEY: str = os.getenv('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    RATELIMIT_DEFAULT: str = "200 per day"
    
class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '../mood_music.db')
    )
    
class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL', '')
    
class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED: bool = False

config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 