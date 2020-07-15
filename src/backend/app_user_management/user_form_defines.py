"""File designed to have 1 point of truth for all form classes
"""
# -- External Packages -- #
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import flash

# -- Project Defined Imports -- #
from backend.app_user_management.user_manager import UserManager

def validate_username(form, field) -> bool:
    """:brief Validates that the username used to login is valid (that it exists with an already created user)
    \n:return True if the username exists for any user"""
    # Determine if the username has been taken
    is_username_in_use = UserManager.does_username_exist(field.data)
    if is_username_in_use is False:
        ValidationError("No account with that username exists. Please try again.")
    return is_username_in_use

class LoginForm(FlaskForm):
    """Represents the creation of a basic login form that is authenticatable by the application"""
    username = StringField('Username', validators=[DataRequired(), validate_username])
    password = PasswordField('Password',  validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    """Represents the creation of a basic registration form that is authenticatable by the application"""
    username = StringField('Username', validators=[DataRequired(), validate_username])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
