from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
from datetime import datetime, timezone
from .utils import clean_html

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
    plan = db.Column(db.String(20), default='free') # User subscription plan
    is_admin = db.Column(db.Boolean, default=False)
    
    def check_plan(self, text, note_count=False):
        """
        Check if user exceeds plan limits
        """
        
        #plan restrictions
        plan = {
                "free": {"max_notes": 10, "max_text_length": 128},
                "pro": {"max_notes": None, "max_text_length": None}
                }
        
        # Clean the text to count real content length
        text_length = len(clean_html(text))


        max_notes = plan[self.plan]["max_notes"]
        max_length = plan[self.plan]["max_text_length"]

        over_note_limit = max_notes is not None and note_count >= max_notes
        over_length_limit = max_length is not None and text_length >= max_length
        
        # Return True if user exceeded restrictions
        return over_note_limit or over_length_limit

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