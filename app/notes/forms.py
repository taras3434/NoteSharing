from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField, HiddenField
from wtforms.validators import InputRequired

class CreateNote(FlaskForm):
    title = StringField(validators=[InputRequired()])
    note = TextAreaField()
    selected_tags = StringField()
    submit = SubmitField("Create note")

class EditNote(FlaskForm):
    title = StringField()
    note = TextAreaField()
    new_editor = StringField()
    save = SubmitField("Save")

class SearchNote(FlaskForm):
    search_field = StringField()
    search = SubmitField("Search note")

class FilterNote(FlaskForm):
    choices = [('val1', 'Newest'), 
               ('val2', 'Oldest'), 
               ('val3', 'Alphabetical A-Z'), 
               ('val4', 'Alphabetical Z-A'), 
               ('val5', 'Favorite')]
    selected_tags = StringField()

    filter_dropdown = SelectField('filter', choices=choices)
