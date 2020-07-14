# -- External Packages -- #
from flask import Flask, redirect, flash
from flask_login import LoginManager, UserMixin
import uuid

# Used by login forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

# -- Project Defined Imports -- #
from backend.app_user_management.user_login import LoginManager
from backend.app_user_management.web_app_user import WebAppUser

class UserManager():
    def __init__(self, app: Flask, send_to_client_func):
        """Class that manages all existing users of the application given a valid Flask app object"""
        # TODO: This will cause interactions with users to have an unfortunately large complexity
        # Maps unique id's -> user objects
        self._users = {}

        self._flask_app = app
        self._send_to_client_func = send_to_client_func
        self._login_manager = LoginManager()
    
    #####################
    # Public Functions  #
    #####################
    def does_username_exist(self, username: str) -> bool():
        """:return True if the username exists for a registerd user"""
        is_user = lambda cur_user: cur_user.username == username
        match_list = list(filter(is_user, self._users.values()))
        return len(match_list) > 0

    def add_user(self, username, password):
        """:brief given a username and password, creates a valid WebAppUser and saves it in the users list"""
        user_token = self._create_new_user_token()
        new_user = WebAppUser(username=username, password=password, user_unique_id=user_token,
                            send_to_client_func=self._send_to_client_func)
        self._users[user_token] = new_user

    def get_login_form(self):
        return self._login_manager.get_login_form()
    

    def get_user_by_username(self, taget_username):
        """:return none if username does not exist"""
        def is_user_target(user: WebAppUser) -> WebAppUser:
            return user.username == taget_username
        # In the case of duplicate usernames, potential users with be a list of more than 1 WebAppUser objects
        potential_users = list(filter(is_user_target, self._users.values()))
        user = potential_users[0] if len(potential_users) > 0 else None
        return user

    def remove_user(self, user_id):
        """:param user_id - A user's unique id / token"""
        #TODO: make a logout client function and call it
        del self._users[user_id]

    ######################
    # Private Functions  #
    ######################
    def _create_new_user_token(self) -> uuid.uuid4:
        """:brief Generates a unique uuid (user token) that can be used by a new user"""
        user_token = None
        # Keep trying to make a token until an unused one is made
        while True:
            user_token = self._generate_safe_cookie_token()
            # Once and unused token is found, return it
            if user_token not in self._users:
                return user_token


    def _generate_safe_cookie_token(self) -> uuid.uuid4:
        """Function to generate a random cookie token (uuid)
        \n:note Info for this function came from - https://docs.python.org/3/library/uuid.html -- safe random uuid
        """
        return str(uuid.uuid4())