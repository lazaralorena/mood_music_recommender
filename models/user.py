from flask_login import UserMixin
from typing import Optional
import bcrypt
from datetime import datetime
from models import db

class User(UserMixin, db.Model):
    """User model for authentication and user management."""
    
    __tablename__ = 'user'
    
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password_hash: bytes = db.Column(db.LargeBinary, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationships
    favorites = db.relationship('Favorite', back_populates='user', lazy=True, cascade='all, delete-orphan')
    favorite_music = db.relationship('Music', secondary='favorite', lazy='dynamic',
                                   backref=db.backref('favorited_by', lazy=True))

    def set_password(self, password: str) -> None:
        """Hash and set the user's password.
        
        Args:
            password: The plain text password to hash
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash.
        
        Args:
            password: The plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def __repr__(self) -> str:
        """String representation of the User model."""
        return f'<User {self.username}>' 