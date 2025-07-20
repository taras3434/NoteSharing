from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import InputRequired

class CreateNote(FlaskForm):
    """
    Form to create a new note.
    """
    title = StringField(validators=[InputRequired()])
    note = TextAreaField()
    submit = SubmitField("Create note")

class EditNote(FlaskForm):
    """
    Form to edit an existing note.
    """
    title = StringField()
    note = TextAreaField()
    save = SubmitField("Save")
