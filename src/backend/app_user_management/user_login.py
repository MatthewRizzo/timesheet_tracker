# -- External Packages -- #
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import flash

# -- Project Defined Imports -- #
from backend.app_user_management.user_manager import UserManager


class LoginManager():
    """Class responsible for all things related to logging in"""
    def __init__(self):
        self._login_form = LoginForm(self.validate_username)

    def validate_username(self, form, field) -> bool():
        """:brief Validates that the username used to login is valid (that it exists with an account)
        \n:return True if the username is valid"""
        # TODO
        pass

    def get_login_form(self) -> LoginForm:
        """:return a valid LoginForm based in FlaskForm
        """
        return self._login_form

class LoginForm(FlaskForm):
    """Represents the creation of a basic login form that is authenticatable by the application"""
    def __init__(self, validate_username_func):
        self.username = StringField('Username', validators=[DataRequired(), validate_username_func])
        self.password = PasswordField('Password',  validators=[DataRequired()])
        self.remember_me = BooleanField('Remember Me')
        self.submit = SubmitField('Submit')