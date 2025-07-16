from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField
from wtforms.validators import InputRequired

class CreateNote(FlaskForm):
    title = StringField(validators=[InputRequired()])
    note = TextAreaField()
    submit = SubmitField("Create note")
    selected_tags = StringField()

class EditNote(FlaskForm):
    title = StringField()
    note = TextAreaField()
    new_editor = StringField()
    save = SubmitField("Save")
