from typing import List, Optional, Dict
import random
from models import Music, Favorite, User, db

class MusicService:
    """Service class for handling music-related operations."""
    
    @staticmethod
    def get_music_by_mood(mood: str) -> List[Dict]:
        """Get all music recommendations based on mood.
        
        Args:
            mood: The mood to find music for
            
        Returns:
            List[Dict]: List of dictionaries containing music information
        """
        musics = Music.query.filter_by(mood=mood.lower()).all()
        return [music.to_dict() for music in musics] if musics else []
    
    @staticmethod
    def get_user_favorites(user: User) -> List[Dict]:
        """Get all favorite songs for a user.
        
        Args:
            user: The user to get favorites for
            
        Returns:
            List[Dict]: List of dictionaries containing favorite music information
        """
        return [music.to_dict() for music in user.favorite_music]
    
    @staticmethod
    def toggle_favorite(user: User, music_id: int) -> tuple[str, bool]:
        """Add or remove a song from user's favorites.
        
        Args:
            user: The user toggling the favorite
            music_id: The ID of the music to toggle
            
        Returns:
            tuple[str, bool]: Message and whether the operation was successful
        """
        music = Music.query.get_or_404(music_id)
        
        if music in user.favorite_music:
            user.favorite_music.remove(music)
            db.session.commit()
            return "Removed from favorites", True
            
        user.favorite_music.append(music)
        db.session.commit()
        return "Added to favorites", True 