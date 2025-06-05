from typing import Optional, Tuple
from models import User, db

class AuthService:
    """Service class for handling authentication and user management."""
    
    @staticmethod
    def register_user(username: str, email: str, password: str) -> Tuple[str, bool]:
        """Register a new user.
        
        Args:
            username: The username for the new user
            email: The email for the new user
            password: The password for the new user
            
        Returns:
            Tuple[str, bool]: Message and whether the registration was successful
        """
        if User.query.filter_by(username=username).first():
            return "Username already exists", False
            
        if User.query.filter_by(email=email).first():
            return "Email already registered", False
            
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return "Registration successful", True
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Tuple[Optional[User], str]:
        """Authenticate a user.
        
        Args:
            username: The username to authenticate
            password: The password to verify
            
        Returns:
            Tuple[Optional[User], str]: User object and message if successful, None and error message if not
        """
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return None, "Invalid username or password"
            
        return user, "Authentication successful" 