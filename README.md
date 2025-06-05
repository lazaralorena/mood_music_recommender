# Mood Music Recommender

A web application that recommends music based on your mood, built with Flask and modern web technologies.

## Features

- Mood-based music recommendations
- User authentication and authorization
- Favorite songs functionality
- Rate limiting and CSRF protection
- Modern, responsive UI with Tailwind CSS
- YouTube integration for music playback

## Security Features

- Secure password hashing with bcrypt
- CSRF protection for all forms and API endpoints
- Rate limiting to prevent abuse
- Environment variables for sensitive data
- Session management with Flask-Login
- Input validation and sanitization

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lazaralorena/mood-music-recommender.git
cd mood-music-recommender
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your configuration
   - Never commit the `.env` file to version control

```bash
cp .env.example .env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
# Generate a secure key using: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=replace_this_with_a_secure_random_key

# Database Configuration
DATABASE_URL=sqlite:///mood_music.db

# Rate Limiting
RATELIMIT_DEFAULT=200 per day
RATELIMIT_STORAGE_URL=memory://
```

5. Initialize the database:
```bash
python app.py
# Visit http://localhost:5000/init-db to populate with sample data
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Visit `http://localhost:5000` in your web browser

## Development

### Setting Up a Development Environment

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

### Security Best Practices

1. Never commit sensitive data:
   - Keep `.env` files local
   - Use environment variables for secrets
   - Don't store API keys in code

2. Regular updates:
   - Keep dependencies updated
   - Check for security advisories
   - Run security audits regularly

3. Code review guidelines:
   - Check for security implications
   - Validate input handling
   - Review authentication logic

## Deployment

### Production Setup

1. Use a production-grade server:
   - Gunicorn or uWSGI
   - Nginx as reverse proxy
   - HTTPS only

2. Environment configuration:
   - Set `FLASK_ENV=production`
   - Use strong secret keys
   - Configure proper logging

3. Database considerations:
   - Use a production database
   - Regular backups
   - Connection pooling

### Security Checklist

- [ ] Configure HTTPS
- [ ] Set secure headers
- [ ] Enable logging
- [ ] Configure backups
- [ ] Set up monitoring
- [ ] Review permissions
- [ ] Update dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Security Issues

For security issues, please:
1. **DO NOT** create a public issue
2. Email security concerns to [lazaracamila@gmail.com]
3. Include detailed information about the vulnerability

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask and its extensions
- Tailwind CSS
- YouTube API
- All contributors and users

## Contact

For questions or feedback, please open an issue or contact lazaracamila@gmail.com. 
