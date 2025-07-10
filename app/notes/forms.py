from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import InputRequired

class CreateNote(FlaskForm):
    title = StringField(validators=[InputRequired()])
    note = TextAreaField()
    submit = SubmitField("Create note")

class EditNote(FlaskForm):
    note = TextAreaField()
    submit = SubmitField("Save note")
    delete = SubmitField("Delete note")