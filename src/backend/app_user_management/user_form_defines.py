"""File designed to have 1 point of truth for all form classes
"""
# -- External Packages -- #
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import flash


class LoginForm(FlaskForm):
    """Represents the creation of a basic login form that is authenticatable by the application"""
    def __init__(self, validate_username_func):
        self.username = StringField('Username', validators=[DataRequired(), validate_username_func])
        self.password = PasswordField('Password',  validators=[DataRequired()])
        self.remember_me = BooleanField('Remember Me')
        self.submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    """Represents the creation of a basic registration form that is authenticatable by the application"""
    def __init__(self, validate_username_func):
        self.username = StringField('Username', validators=[DataRequired(), validate_username_func])
        self.password = PasswordField('Password', validators=[DataRequired()])
        self.password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
        self.submit = SubmitField('Register')