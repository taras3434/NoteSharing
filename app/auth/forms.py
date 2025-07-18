from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    """
    User registration form with username and password fields
    """
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)])

    submit = SubmitField("Register")

    def validate_username(self, username):
        """
        Validator to check if the username already exists in the database
        """
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already exists.")
        
class LoginForm(FlaskForm):
    """
    User login form with username and password fields.
    """
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)])
    
    submit = SubmitField("Login")

class ChangePasswordForm(FlaskForm):
    """
    Form to change user password.
    """
    old_password = StringField(validators=[InputRequired(), Length(min=8, max=20)])
    new_password = StringField(validators=[InputRequired(), Length(min=8, max=20)])

    submit = SubmitField("Change password")
