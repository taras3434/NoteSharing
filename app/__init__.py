from flask import Flask, send_from_directory
from .notes import notes_bp
from .auth import auth_bp
from .home import home_bp
from .models import db, migrate, User, Note, NoteVersion
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class='config.Config'):
    app = Flask(__name__)

    app.register_blueprint(notes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    admin = Admin(app, name='Note Admin', template_mode='bootstrap4')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Note, db.session))
    admin.add_view(ModelView(NoteVersion, db.session))

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/x-icon')
    return app