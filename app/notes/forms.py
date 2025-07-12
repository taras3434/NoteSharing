from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField
from wtforms.validators import InputRequired

class CreateNote(FlaskForm):
    title = StringField(validators=[InputRequired()])
    note = TextAreaField()
    submit = SubmitField("Create note")

class EditNote(FlaskForm):
    title = StringField()
    note = TextAreaField()
    save = SubmitField("Save")
    delete = SubmitField("Delete note")

class SearchNote(FlaskForm):
    search_field = StringField()
    search = SubmitField("Search note")

class FilterNote(FlaskForm):
    choices = [('val1', 'Newest'), ('val2', 'Oldest'), ('val3', 'Alphabetical A-Z'), ('val4', 'Alphabetical Z-A')]
    filter_dropdown = SelectField('filter', choices=choices)
