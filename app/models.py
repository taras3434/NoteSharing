from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
from datetime import datetime, timezone
from .utils import clean_html

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    plan = db.Column(db.String(50), default='free')

    def check_plan(self, text, note_count=False):
        plan = {"free" : {"max_notes" : 10, "max_text_length" : 128}}
        
        text_length = len(clean_html(text))

        return (note_count >= plan[self.plan]["max_notes"]) or (text_length >= plan[self.plan]["max_text_length"])

class Note(db.Model):
    id = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='notes')
    title = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_edit = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    text = db.Column(db.Text, nullable=False) 
    is_favorite = db.Column(db.Boolean, default=False)

class NoteVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    text = db.Column(db.Text, nullable=False) 