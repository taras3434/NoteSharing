from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField

class CreateNote(FlaskForm):
    note = TextAreaField()
    submit = SubmitField("Create note")
