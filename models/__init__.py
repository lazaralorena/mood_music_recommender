from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .music import Music
from .favorite import Favorite

__all__ = ['db', 'User', 'Music', 'Favorite'] 