from flask import Flask, send_from_directory
from .notes import notes_bp # Notes-related routes 
from .auth import auth_bp # Authentication routes 
from .home import home_bp # Home page routes
from .models import db, migrate, User, Note, NoteVersion # Database models
from .admin import NoteAdminIndexView, AdminModelView
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

# Initialize Flask-Login
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class='config.Config'):
    """
    Initialize and return the Flask application instance
    """
    app = Flask(__name__)

    # Register route blueprints
    app.register_blueprint(notes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    # Load configuration from config class
    app.config.from_object(config_class)

    # Initialize database and migration support
    db.init_app(app)
    migrate.init_app(app, db)

    # Set up Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "auth.login" # Redirect to login view if unauthorized
    
    # Set up Flask-Admin 
    admin = Admin(app, name='Note Admin', index_view=NoteAdminIndexView(), template_mode='bootstrap4')
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Note, db.session))
    admin.add_view(AdminModelView(NoteVersion, db.session))
    
    # Favicon route
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/x-icon')
    return app