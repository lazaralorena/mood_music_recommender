import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Music

def init_db():
    """Initialize the database with sample music data."""
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data
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
            # Nostalgic songs
            Music(title='Sweet Dreams', artist='Eurythmics', mood='nostalgic', url='https://www.youtube.com/watch?v=qeMFqkcPYcg'),
            Music(title='Take On Me', artist='a-ha', mood='nostalgic', url='https://www.youtube.com/watch?v=djV11Xbc914'),
            Music(title='Billie Jean', artist='Michael Jackson', mood='nostalgic', url='https://www.youtube.com/watch?v=Zi_XLOBDo_Y'),
            Music(title='Sweet Child O Mine', artist='Guns N Roses', mood='nostalgic', url='https://www.youtube.com/watch?v=1w7OgIMMRc4'),
            # Chill songs
            Music(title='Waves', artist='Mr Probz', mood='chill', url='https://www.youtube.com/watch?v=pUjE9H8QlA4'),
            Music(title='Midnight City', artist='M83', mood='chill', url='https://www.youtube.com/watch?v=dX3k_QDnzHE'),
            Music(title='Breathe', artist='Télépopmusik', mood='chill', url='https://www.youtube.com/watch?v=vyut3GyQtn0'),
            Music(title='Porcelain', artist='Moby', mood='chill', url='https://www.youtube.com/watch?v=IJWlBfo5Oj0')
        ]
        
        for music in sample_data:
            db.session.add(music)
            
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_db() 