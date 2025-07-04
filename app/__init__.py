from flask import Flask
from .notes import notes_bp
from .auth import auth_bp  
from .models import db

def create_app():
    app = Flask(__name__)

    app.register_blueprint(notes_bp)
    app.register_blueprint(auth_bp)
    #TODO config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
    app.config['SECRET_KEY'] = 'your-secret-key'
    #TODO flask-migrate
    db.init_app(app)

    return app