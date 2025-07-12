from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField(validators=[InputRequired(), Length(min=1, max=20)])

    submit = SubmitField("Register")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already exists.")
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField(validators=[InputRequired(), Length(min=1, max=20)])

    submit = SubmitField("Login")

class ChangePasswordForm(FlaskForm):
    old_password = StringField(validators=[InputRequired(), Length(min=1, max=20)])
    new_password = StringField(validators=[InputRequired(), Length(min=1, max=20)])

    submit = SubmitField("Change password")
