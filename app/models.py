from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
from datetime import datetime, timezone

# Initialize database and migration objects
db = SQLAlchemy()
migrate = Migrate()

class User(db.Model, UserMixin):
    """
    User model representing a registered user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) # Unique username
    password_hash = db.Column(db.String(128), nullable=False) # Hashed password
    is_admin = db.Column(db.Boolean, default=False)

class Note(db.Model):
    """
    Note model representing a note created by a user.
    """
    id = db.Column(db.String(64), primary_key=True, unique=True, nullable=False) # Unique UUID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign key to User
    user = db.relationship('User', backref='notes') # Relationship to User model (one-to-many)
    title = db.Column(db.String(64), nullable=False) # Note title
    start_date = db.Column(db.DateTime, default=datetime.now(timezone.utc)) # Creation date/time in UTC
    last_edit = db.Column(db.DateTime, default=datetime.now(timezone.utc)) # Last modification date/time in UTC
    text = db.Column(db.Text, nullable=False) # Note content
    is_favorite = db.Column(db.Boolean, default=False) # Flag for marking note as favorite for user
    
class NoteVersion(db.Model):
    """
    NoteVersion model stores history of notes editing.
    """
    id = db.Column(db.Integer, primary_key=True) # Auto-incremented version ID
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False) # Foreign key to the original Note
    text = db.Column(db.Text, nullable=False) #Note text
    version_date = db.Column(db.DateTime, default=datetime.now(timezone.utc)) #When this version was saved