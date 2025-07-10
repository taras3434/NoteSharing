from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

#TODO free and pro plan

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    plan = db.Column(db.String(50), default='free')

    def check_plan(self, note_count):
        plan = {"free" : 10}
        return note_count >= plan[self.plan]

class Note(db.Model):
    id = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='notes')
    title = db.Column(db.String(64), nullable=False)
    #TODO start_date
    #TODO last_edit
    text = db.Column(db.Text, nullable=False) 