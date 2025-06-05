from typing import Optional
from datetime import datetime
from models import db

class Music(db.Model):
    """Music model for storing song information."""
    
    __tablename__ = 'music'
    
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(100), nullable=False)
    artist: str = db.Column(db.String(100), nullable=False)
    mood: str = db.Column(db.String(50), nullable=False)
    url: str = db.Column(db.String(200), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationships
    favorites = db.relationship('Favorite', back_populates='music', lazy=True, cascade='all, delete-orphan')

    def to_dict(self) -> dict:
        """Convert the music object to a dictionary.
        
        Returns:
            dict: Dictionary representation of the music
        """
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'mood': self.mood,
            'url': self.url
        }

    def __repr__(self) -> str:
        """String representation of the Music model."""
        return f'<Music {self.title} by {self.artist}>' 