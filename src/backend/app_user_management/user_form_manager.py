# -- External Packages -- #
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import flash

# -- Project Defined Imports -- #
from backend.app_user_management.user_form_defines import LoginForm, RegistrationForm

class UserFormManager():
    """Class responsible for all things related to logging in
    \n:param does_username_exist_func - Returns true if the username has been taken by a user. Takes username as input
    """
    def __init__(self, does_username_exist_func):
        self._does_username_exist_func = does_username_exist_func

        # Create both types of form
        self._login_form = LoginForm(self.validate_username)
        self._regisration_form = RegistrationForm(self.validate_username)


    #####################
    # Public Functions  #
    #####################
    def validate_username(self, form, field) -> bool:
        """:brief Validates that the username used to login is valid (that it exists with an already created user)
        \n:return True if the username exists for any user"""
        # Determine if the username has been taken
        is_username_in_use = self._does_username_exist_func(field.data)
        if is_username_in_use is False:
            ValidationError("No account with that username exists. Please try again.")
        return is_username_in_use

    def get_login_form(self) -> LoginForm:
        """:return a valid LoginForm based in FlaskForm"""
        return self._login_form

    def get_registration_form(self) -> RegistrationForm:
        """:return a valid RegistrationForm based in FlaskForm"""
        return self._regisration_form

    ######################
    # Private Functions  #
    ######################
# End of UserFormManager Class