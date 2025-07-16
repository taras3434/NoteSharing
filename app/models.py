from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
from datetime import datetime, timezone
from .utils import clean_html

db = SQLAlchemy()
migrate = Migrate()

note_tag = db.Table('note_tag',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

editor = db.Table('editor',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    plan = db.Column(db.String(50), default='free')
    editable_notes = db.relationship('Note', secondary=editor, back_populates='editors')

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
    tags = db.relationship('Tag', secondary=note_tag, back_populates='notes')
    editors = db.relationship('User', secondary=editor, back_populates='editable_notes')
    
class NoteVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    text = db.Column(db.Text, nullable=False) 
    version_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(64), unique=True)
    notes = db.relationship('Note', secondary=note_tag, back_populates='tags')