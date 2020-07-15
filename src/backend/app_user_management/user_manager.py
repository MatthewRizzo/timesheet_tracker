# -- External Packages -- #
import pathlib
from flask import Flask, redirect, flash
from flask_login import LoginManager, UserMixin
import uuid

# Used by login forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

# -- Project Defined Imports -- #
from backend import constants
from backend.app_user_management.user_form_manager import UserFormManager
from backend.app_user_management.user_form_defines import RegistrationForm, LoginForm
from backend.app_user_management.web_app_user import WebAppUser
from backend import utils

class UserManager():
    def __init__(self, app: Flask, send_to_client_func):
        """Class that manages all existing users of the application given a valid Flask app object"""
        # Save inputs  to class
        self._flask_app = app
        self._send_to_client_func = send_to_client_func

        # TODO: This will cause interactions with users to have an unfortunately large complexity
        # Maps unique id's -> user objects
        self._users = {}

        # Create and save objects using inputs
        self._login_manager = LoginManager(app)
        self._user_form_manager = UserFormManager(self.does_username_exist)

        self._create_cookie_data_file()
        self._create_login_manager()
    
    #####################
    # Public Functions  #
    #####################
    def does_username_exist(self, username: str) -> bool():
        """:return True if the username is already in use by another user"""
        # If this returns a user, the username is a duplicate. If it returns none, it has yet to be used
        user = self.get_user_by_username()
        # only returns None when the username does not exist
        if user is None:
            return False
        else:
            return True

    def add_user(self, username, password):
        """:brief given a username and password, creates a valid WebAppUser and saves it in the users list"""
        # If the username is already being used, don't let this go through as is
        if self.does_username_exist() is True:
            flash("Username is already taken. Please try again.")
        user_token = self._create_new_user_token()

        # Create a new user based on the information gathered
        new_user = WebAppUser(username=username, password=password, user_unique_id=user_token,
                            send_to_client_func=self._send_to_client_func)
        self._users[user_token] = new_user


    def get_login_form(self) -> LoginForm:
        return self._user_form_manager.get_login_form()

    def get_registration_form(self) -> RegistrationForm:
        return self._user_form_manager.get_registration_form()

    def get_user_login(self, user_id) -> dict():
        """:brief: Get the user's login username and password based on their browser's cookie
        \n:param: `user_id` The user's id (token) retrieved from cookie
        \n:note: username & password login is specifically for the app managed by app_manager
        \n:note: `userToken` is the user's unique token based on browser and cookie data
        \n:return: {username: str, password: str}
        """
        cookie_dict = utils.load_json(constants.PATH_TO_COOKIES_DATA)
        return cookie_dict

    def get_user_by_username(self, taget_username) -> WebAppUser:
        """:return None if username does not exist. Otherwise a WebAppUser object"""
        def is_user_target(user: WebAppUser) -> WebAppUser:
            return user.username == taget_username
        # In the case of duplicate usernames, potential users with be a list of more than 1 WebAppUser objects
        potential_users = list(filter(is_user_target, self._users.values()))
        user = potential_users[0] if len(potential_users) > 0 else None
        return user

    def remove_user(self, user_id):
        """:param `user_id` - A user's unique id / token"""
        #TODO: make a logout client function and call it
        del self._users[user_id]

    ######################
    # Private Functions  #
    ######################
    def _create_cookie_data_file(self):
        """Utility function to check if cookie file exists already or not. If it doesn't, the file gets created"""
        path_to_user_dir = constants.PATH_TO_USER_DATA
        path_to_cookie_file = constants.PATH_TO_COOKIES_DATA
        constants.PATH_TO_COOKIES_DATA
        # Create path to parent dir of file
        if path_to_user_dir.exists is False:
            path_to_user_dir.mkdir(parents=True)

        # If the file itself does not exist, create it
        if path_to_cookie_file.exists() is False:
            utils.write_to_json(path_to_cookie_file, {})

    def _create_login_manager(self):
        """\n:brief: Helper function that links all the necessary login (callbacks) from flask login
        \n:note: Wrapper to provide closure for `self`"""

        @self._login_manager.user_loader
        def load_user(user_token):
            """ \nbrief - When Flask app is asked for "current_user", this decorator gets the current user's User object
                \nnote - Reference current user with `current_user` (from flask_login import current_user) 
                \nparam - `user_token` - The user's unique token id
                \nreturn - The WebAppUser object corresponding to the `user_token` given
            """
            return self._users[user_token]

        @self._login_manager.unauthorized_handler
        def on_need_to_login():
            """\n:brief: VERY important. This callback  redirects the user to login if needed.
                "@login_required" triggers this function if page is accessed without logging in
            """
            return redirect(constants.SITE_PATHS["login"])

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