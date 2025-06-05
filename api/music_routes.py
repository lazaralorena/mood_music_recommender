from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from services.music_service import MusicService
from models import db, Music, User

music_bp = Blueprint('music', __name__, url_prefix='/api/music')

@music_bp.route('/<mood>', methods=['GET'])
@login_required
def get_music_by_mood(mood: str):
    """Get music recommendations by mood.
    
    Args:
        mood: The mood to get music recommendations for
    """
    try:
        music = MusicService.get_music_by_mood(mood)
        if not music:
            return jsonify({'error': 'No music found for this mood'}), 404
        return jsonify(music)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@music_bp.route('/favorite/<int:music_id>', methods=['POST', 'DELETE'])
@login_required
def manage_favorite(music_id: int):
    """Add or remove a song from user's favorites.
    
    Args:
        music_id: The ID of the music to manage
    """
    try:
        if request.method == 'DELETE':
            music = Music.query.get_or_404(music_id)
            if music not in current_user.favorite_music:
                return jsonify({'message': 'Song was not in favorites'}), 404
            current_user.favorite_music.remove(music)
            db.session.commit()
            return jsonify({'message': 'Successfully removed from favorites'}), 200
        else:  # POST
            message, success = MusicService.toggle_favorite(current_user, music_id)
            if not success:
                return jsonify({'error': message}), 400
            return jsonify({'message': message})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@music_bp.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    """Get all favorite songs for the current user."""
    try:
        favorites = MusicService.get_user_favorites(current_user)
        return jsonify(favorites)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500 