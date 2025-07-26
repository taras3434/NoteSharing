from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import InputRequired

class CreateNote(FlaskForm):
    """
    Form to create a new note.
    """
    title = StringField(validators=[InputRequired()])
    note = TextAreaField(render_kw={"x-ref": "noteHiddenField"})
    submit = SubmitField("Create note")

class EditNote(FlaskForm):
    """
    Form to edit an existing note.
    """
    title = StringField(render_kw={"x-ref": "editTitleInput"})
    note = TextAreaField()
    save = SubmitField("Save")
