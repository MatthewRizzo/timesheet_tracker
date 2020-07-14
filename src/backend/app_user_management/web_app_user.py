# -- External Packages -- #
from flask import Flask, redirect, flash
from flask_login import LoginManager, UserMixin

# -- Project Defined Imports -- #
from backend.backend_controller import BackendController

class WebAppUser(UserMixin):
    """Class defining what a "user" actually is.
    \n:parma send_to_client_func - The function from app_manager capable of sending messages up a socket to the frontend
    \n:param user_unique_id - A unique id given to each user

    """
    def __init__(self, username: str, password: str, user_unique_id, send_to_client_func: function):
        self.username = username
        self.password = password
        self.backend_controller = BackendController(send_to_client=send_to_client_func, username=self.username)

        # Required by extension of UserMixin 
        self.id = user_unique_id 
