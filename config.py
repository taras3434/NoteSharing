import os

# Get the absolute path of the current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key used for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

    # Database connection URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///notes.db'

    #Bootstrap theme for Flask-Admin UI
    FLASK_ADMIN_SWATCH = 'litera'