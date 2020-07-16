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
from backend.app_user_management.web_app_user import WebAppUser
from backend import utils

class UserManager():
    """Class that manages all existing users of the application given a valid Flask app object.
    \n:note Has some class methods in order to provide a validation function to FlaskForm's"""
    # TODO: This will cause interactions with users to have an unfortunately large complexity
    # Maps unique id's -> user objects. 
    _users_being_managed = {}
    
    # Used to keep track of valid usernames
    _valid_users_names = []
    _path_to_cookie_file = constants.PATH_TO_COOKIES_DATA

    def __init__(self, app: Flask, send_to_client_func):

        # Save inputs  to class
        self._send_to_client_func = send_to_client_func
        self._login_manager = LoginManager(app)

        self._manage_cookie_data_file()
        self._create_login_manager()
    #####################
    # Public Functions  #
    #####################
    @classmethod
    def does_username_exist(cls, username: str) -> bool():
        """:return True if the username is already in use by another user.
        \n:note Used as valdiate function by FlaskForm's"""
        # Check the list of users
        return username in UserManager._valid_users_names


    def add_user(self, username, password):
        """:brief given a username and password, creates a valid WebAppUser and saves it in the users list"""
        # If the username is already being used, don't let this go through as is
        if self.does_username_exist(username) is True:
            flash("Username is already taken. Please try again.")
        user_token = self._create_new_user_token()

        # Create a new user based on the information gathered (adds it to internal data structures)
        new_user = self._create_user(username, password, user_token)
        UserManager._valid_users_name.append(username)

        # Update the cookie file with the new users
        self._add_to_cookie_file(username, password, user_token)

    def login_user(self, username) -> WebAppUser:
        """:brief - Creates a WebAppUser object of the user with the given username. Adds it to tracked users list.
        \n:param username - The user to login
        \n:precondition - The username is a valid user in the cookie file
        \n:return - The `WebAppUser` logged in"""
        # Get user_token first to speed up getting the password
        user_token = self._get_user_token_by_username(username)
        password = self._get_user_password(username, user_token=user_token)
        logged_in_user = self._create_user(username, password, user_token)
        return logged_in_user

    def get_user_login(self, user_id) -> dict():
        """:brief: Get the user's login username and password based on their browser's cookie
        \n:param: `user_id` The user's id (token) retrieved from cookie
        \n:note: username & password login is specifically for the app managed by app_manager
        \n:note: `userToken` is the user's unique token based on browser and cookie data
        \n:return: {username: str, password: str}
        """
        cookie_dict = utils.load_json(UserManager._path_to_cookie_file)
        return cookie_dict[user_id]

    @classmethod
    def get_user_by_username(cls, target_username) -> WebAppUser:
        """:return None if username does not exist. Otherwise a WebAppUser object"""
        def is_user_target(user: WebAppUser) -> WebAppUser:
            return user.username == target_username
        # In the case of duplicate usernames, potential users with be a list of more than 1 WebAppUser objects
        potential_users = list(filter(is_user_target, UserManager._users_being_managed.values()))
        user = potential_users[0] if len(potential_users) > 0 else None
        return user

    def remove_user(self, user_id):
        """:param `user_id` - A user's unique id / token"""
        #TODO: make a logout client function and call it
        username = self.get_username(user_id)
        del UserManager._users_being_managed[user_id]
        if username in UserManager._valid_users_names:
            UserManager._valid_users_names.remove(username)

    def get_username(self, user_id):
        """Given a user_id, returns the user's username"""
        return UserManager._users_being_managed[user_id].get_username()

    def is_password_valid(self, username, password):
        """Given a `username` ensures the password given is valid
        \n:return `True` if `password` is correct for `username`
        \n:precondition - `username` is a valid username for a user"""
        desired_password = self._get_user_password(username)
        return desired_password == password
    ######################
    # Private Functions  #
    ######################
    def _add_to_cookie_file(self, username, password, user_token):
        """:brief Grabs the current cookie file and adds the new user to it"""
        # Get the current set of cookies
        cur_user_dict = utils.load_json(UserManager._path_to_cookie_file)

        # Add the new cookie for the user
        cur_user_dict[user_token] = dict()
        cur_user_dict[user_token]['username'] = username
        cur_user_dict[user_token]['password'] = password

        # Rewrite the data to the file (with the new addition)
        utils.write_to_json(UserManager._path_to_cookie_file, cur_user_dict)

    def _create_user(self, username, password, user_token) -> WebAppUser:
        """:brief - Utility function to create a user object and add it to tracked _users_being_managed
        \n:return the `WebAppUser` created"""
        new_user = WebAppUser(username=username, password=password, user_unique_id=user_token,
                            send_to_client_func=self._send_to_client_func)
        UserManager._users_being_managed[user_token] = new_user
        return new_user

    def _manage_cookie_data_file(self):
        """Utility function to check if cookie file exists already or not. 
            If it doesn't, the file gets created. Otherwise, its data is loaded in
        \n:note If the file exists, its usernames are added to _valid_users_names"""
        path_to_user_dir = constants.PATH_TO_USER_DATA
        path_to_cookie_file = UserManager._path_to_cookie_file

        # If the cookie file exists already, load in its data
        if path_to_cookie_file.exists() is True:
            cookie_data_dict = utils.load_json(path_to_cookie_file)
            for user_token in cookie_data_dict.keys():
                username = cookie_data_dict[user_token]['username']
                UserManager._valid_users_names.append(username)
            return

        # Create path to parent dir of file
        if path_to_user_dir.exists() is False:
            path_to_user_dir.mkdir(parents=True)
        if path_to_cookie_file.exists() is False:
            # If the file itself does not exist, create it
            utils.write_to_json(path_to_cookie_file, {})

    def _get_user_password(self, username: str, user_token=None) -> str:
        """:brief - Utility function to get a user's password based on their username or user_token
        \n:note - If `user_token` is given, skips finding it (saves computation time). Else will find it using username
        \n:param `user_token` - When given, reduces time complexity by getting the user data from cookie
        \n:param `username` - The name of the user whose password needs to be retrieved"""
        if user_token is None:
            user_token = self._get_user_token_by_username(username)
        login_dict = self.get_user_login(user_token)
        password = login_dict['password']
        return password

    def _get_user_token_by_username(self, username: str) -> uuid.uuid4:
        """:brief - Utility function to get a user's token based on their username"""
        cookie_data = utils.load_json(UserManager._path_to_cookie_file)
        is_target_user = lambda user_token: cookie_data[user_token]['username'] == username
        user_token = list(filter(is_target_user, cookie_data.keys()))[0]
        return user_token

    def _create_new_user_token(self) -> uuid.uuid4:
        """:brief Generates a unique uuid (user token) that can be used by a new user"""
        user_token = None
        # Keep trying to make a token until an unused one is made
        while True:
            user_token = self._generate_safe_cookie_token()
            # Once and unused token is found, return it
            if user_token not in UserManager._users_being_managed:
                return user_token

    def _generate_safe_cookie_token(self) -> uuid.uuid4:
        """Function to generate a random cookie token (uuid)
        \n:note Info for this function came from - https://docs.python.org/3/library/uuid.html -- safe random uuid
        """
        return str(uuid.uuid4())


    ###########################################
    # DO NOT TOUCH - WRAPPERS NEEDED BY FLASK #
    ###########################################
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
            return UserManager._users_being_managed[user_token]

        @self._login_manager.unauthorized_handler
        def on_need_to_login():
            """\n:brief: VERY important. This callback  redirects the user to login if needed.
                "@login_required" triggers this function if page is accessed without logging in
            """
            return redirect(constants.SITE_PATHS["login"])

