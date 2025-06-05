from typing import Optional
from datetime import datetime
from models import db

class Favorite(db.Model):
    """Favorite model for storing user's favorite songs."""
    
    __tablename__ = 'favorite'
    
    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    music_id: int = db.Column(db.Integer, db.ForeignKey('music.id', ondelete='CASCADE'), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationships
    music = db.relationship('Music', back_populates='favorites')
    user = db.relationship('User', back_populates='favorites')

    def __repr__(self) -> str:
        """String representation of the Favorite model."""
        return f'<Favorite user_id={self.user_id} music_id={self.music_id}>' 