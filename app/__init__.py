from flask import Flask
from .notes import notes_bp
from .auth import auth_bp
from .home import home_bp
from .models import db, User
from flask_login import LoginManager

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    app.register_blueprint(notes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    #TODO config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
    app.config['SECRET_KEY'] = 'your-secret-key'
    #TODO flask-migrate
    db.init_app(app)
    login_manager.init_app(app)
    
    return app