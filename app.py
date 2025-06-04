from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
import bcrypt
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Security configurations
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
csrf = CSRFProtect(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[os.getenv('RATELIMIT_DEFAULT', "200 per day")]
)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'mood_music.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

# Music Model
class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)

# Favorite Model for saving user's favorite songs
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'), nullable=False)
    music = db.relationship('Music', backref='favorites')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('home'))

@app.route('/api/music/<mood>', methods=['GET'])
@login_required
@limiter.limit("30 per minute")
def get_music_by_mood(mood):
    try:
        musics = Music.query.filter_by(mood=mood.lower()).all()
        if not musics:
            print(f"No music found for mood: {mood}")
            return jsonify({'error': 'No music found for this mood'}), 404
        
        random_music = random.choice(musics)
        print(f"Returning music: {random_music.title} for mood: {mood}")
        return jsonify({
            'id': random_music.id,
            'title': random_music.title,
            'artist': random_music.artist,
            'mood': random_music.mood,
            'url': random_music.url
        })
    except Exception as e:
        print(f"Error getting music: {e}")
        return jsonify({'error': 'Database error occurred'}), 500

@app.route('/api/favorite/<int:music_id>', methods=['POST', 'DELETE'])
@login_required
@limiter.limit("30 per minute")
def manage_favorite(music_id):
    try:
        if request.method == 'POST':
            if not Favorite.query.filter_by(user_id=current_user.id, music_id=music_id).first():
                favorite = Favorite(user_id=current_user.id, music_id=music_id)
                db.session.add(favorite)
                db.session.commit()
                return jsonify({'message': 'Added to favorites'})
            return jsonify({'message': 'Already in favorites'})
        
        elif request.method == 'DELETE':
            favorite = Favorite.query.filter_by(user_id=current_user.id, music_id=music_id).first()
            if favorite:
                db.session.delete(favorite)
                db.session.commit()
                return jsonify({'message': 'Removed from favorites'})
            return jsonify({'message': 'Not in favorites'}), 404

    except Exception as e:
        print(f"Error managing favorite: {e}")
        return jsonify({'error': 'Database error occurred'}), 500

@app.route('/api/favorites', methods=['GET'])
@login_required
def get_favorites():
    try:
        favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': fav.music.id,
            'title': fav.music.title,
            'artist': fav.music.artist,
            'mood': fav.music.mood,
            'url': fav.music.url
        } for fav in favorites])
    except Exception as e:
        print(f"Error getting favorites: {e}")
        return jsonify({'error': 'Database error occurred'}), 500

@app.route('/init-db')
def init_db():
    try:
        db.drop_all()
        db.create_all()
        
        # Add sample music data
        sample_data = [
            Music(title='Happy', artist='Pharrell Williams', mood='happy', url='https://www.youtube.com/watch?v=ZbZSe6N_BXs'),
            Music(title='Dont Stop Believin', artist='Journey', mood='happy', url='https://www.youtube.com/watch?v=1k8craCGpgs'),
            Music(title='Walking on Sunshine', artist='Katrina & The Waves', mood='happy', url='https://www.youtube.com/watch?v=iPUmE-tne5U'),
            Music(title='Uptown Funk', artist='Mark Ronson ft. Bruno Mars', mood='happy', url='https://www.youtube.com/watch?v=OPf0YbXqDm0'),
            Music(title='Someone Like You', artist='Adele', mood='sad', url='https://www.youtube.com/watch?v=hLQl3WQQoQ0'),
            Music(title='All By Myself', artist='Celine Dion', mood='sad', url='https://www.youtube.com/watch?v=NGrLb6W5YOM'),
            Music(title='Say Something', artist='A Great Big World & Christina Aguilera', mood='sad', url='https://www.youtube.com/watch?v=-2U0Ivkn2Ds'),
            Music(title='Fix You', artist='Coldplay', mood='sad', url='https://www.youtube.com/watch?v=k4V3Mo61fJM'),
            Music(title='Eye of the Tiger', artist='Survivor', mood='energetic', url='https://www.youtube.com/watch?v=btPJPFnesV4'),
            Music(title='Cant Hold Us', artist='Macklemore', mood='energetic', url='https://www.youtube.com/watch?v=2zNSgSzhBfM'),
            Music(title='Stronger', artist='Kanye West', mood='energetic', url='https://www.youtube.com/watch?v=PsO6ZnUZI0g'),
            Music(title='Titanium', artist='David Guetta ft. Sia', mood='energetic', url='https://www.youtube.com/watch?v=JRfuAukYTKg'),
            Music(title='Peaceful Piano', artist='Various Artists', mood='relaxed', url='https://www.youtube.com/watch?v=XULUBg_ZcAU'),
            Music(title='River Flows in You', artist='Yiruma', mood='relaxed', url='https://www.youtube.com/watch?v=7maJOI3QMu0'),
            Music(title='Weightless', artist='Marconi Union', mood='relaxed', url='https://www.youtube.com/watch?v=UfcAVejslrU'),
            Music(title='Experience', artist='Ludovico Einaudi', mood='relaxed', url='https://www.youtube.com/watch?v=_VONMkKkdf4'),
            Music(title='All of Me', artist='John Legend', mood='romantic', url='https://www.youtube.com/watch?v=450p7goxZqg'),
            Music(title='Perfect', artist='Ed Sheeran', mood='romantic', url='https://www.youtube.com/watch?v=2Vv-BfVoq4g'),
            Music(title='At Last', artist='Etta James', mood='romantic', url='https://www.youtube.com/watch?v=S-cbOl96RFM'),
            Music(title='Thinking Out Loud', artist='Ed Sheeran', mood='romantic', url='https://www.youtube.com/watch?v=lp-EO5I60KA'),
            Music(title='Time', artist='Hans Zimmer', mood='focused', url='https://www.youtube.com/watch?v=RxabLA7UQ9k'),
            Music(title='Strobe', artist='Deadmau5', mood='focused', url='https://www.youtube.com/watch?v=tKi9Z-f6qX4'),
            Music(title='Brain Waves', artist='Alpha Waves', mood='focused', url='https://www.youtube.com/watch?v=WPni755-Krg'),
            Music(title='Focus', artist='Hania Rani', mood='focused', url='https://www.youtube.com/watch?v=kFRdoYfZYUY'),
            Music(title='Sweet Dreams (Are Made of This)', artist='Eurythmics', mood='nostalgic', url='https://www.youtube.com/watch?v=qeMFqkcPYcg'),
            Music(title='Take on Me', artist='a-ha', mood='nostalgic', url='https://www.youtube.com/watch?v=djV11Xbc914'),
            Music(title='Africa', artist='Toto', mood='nostalgic', url='https://www.youtube.com/watch?v=FTQbiNvZqaY'),
            Music(title='Dreams', artist='Fleetwood Mac', mood='nostalgic', url='https://www.youtube.com/watch?v=mrZRURcb1cM'),
            Music(title='Midnight City', artist='M83', mood='chill', url='https://www.youtube.com/watch?v=dX3k_QDnzHE'),
            Music(title='Waves', artist='Mr Probz', mood='chill', url='https://www.youtube.com/watch?v=pUjE9H8QlA4'),
            Music(title='Sunday Morning', artist='Maroon 5', mood='chill', url='https://www.youtube.com/watch?v=S2Cti12XBw4'),
            Music(title='Breathe', artist='Télépopmusik', mood='chill', url='https://www.youtube.com/watch?v=vyut3GyQtn0')
        ]
        
        for music in sample_data:
            db.session.add(music)
        db.session.commit()
        print("Database reinitialized with sample data!")
        return jsonify({'message': 'Database initialized successfully!'})
    except Exception as e:
        print(f"Error initializing database: {e}")
        return jsonify({'error': f'Failed to initialize database: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 