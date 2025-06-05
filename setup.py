from setuptools import setup, find_packages

setup(
    name="mood_music_recommender",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-login',
        'flask-cors',
        'flask-limiter',
        'flask-wtf',
        'bcrypt',
        'python-dotenv'
    ]
) 