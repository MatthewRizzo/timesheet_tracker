"""File responsible for all flask routes"""
# -- External Packages -- #
import flask
from flask import request, Flask, render_template, send_from_directory, jsonify, redirect, flash
from flask_socketio import SocketIO
from flask_login import login_user, current_user, login_required, logout_user
import logging
import secrets # Used to create a secure secret key (used by flask's application)
import os
import webbrowser

# Used to wrap App in a secure production server environment
import werkzeug.serving 

# -- Project Defined Imports -- #
from backend.backend_controller import BackendController
from backend import constants
from backend.app_user_management.user_manager import UserManager
from backend.app_user_management import user_form_defines

class AppManager():
    """Class responsible for setting up the Flask app and managing all the routes / sockets"""
    def __init__(self):
        self.sites = constants.SITE_PATHS
        self.form_sites = self.sites["form_sites"]

        self._setup_app_config()

        # TODO - implement a way for users to login. It will change this variable (will have to propoagate to backend as well)
        # self._user = "General"

        # TODO - have this get controlled via an input
        self._debug = False

        # Used to communicate from backend->frontend js
        self._socketio = SocketIO(self._app, async_mode="threading")
        self._create_url()
        self.user_manager = UserManager(app=self._app, send_to_client_func=self._send_to_client)

        # self.controller = BackendController(self._send_to_client, self._user)

        # Setup App Routes
        self.create_routes()

    def create_routes(self):
        """Wrapper function for all the routes that need to be created
        """
        self._create_registration_routes()
        self._create_login_routes()
        self._create_mainpage_routes()
        self._create_task_selection_routes()
        self._create_timer_routes()
        self._create_time_display_routes()

    def _send_to_client(self, message_name, content_json=None):
        """Function to enable communication from backend to front-end via sockets"""
        if content_json:
            self._socketio.emit(message_name, content_json)
        else:
            self._socketio.emit(message_name)

    def _create_mainpage_routes(self):
        @self._app.route(self.sites["landing_page"])
        def landing_page():
            """This is the page users will have access to before logging in. It allows them to register and or login"""
            return render_template("landing_page.html", title="Timesheet Tracker About Page", links=self.sites, form_links=self.form_sites)
            

        @login_required
        @self._app.route(self.sites["homepage"])
        def homepage():
            return render_template("index.html")

        @self._app.route("/favicon.ico")
        def favicon():
            return send_from_directory(self._images_dir, 'stopwatch.png', mimetype='image/vnd.microsoft.icon')

        @login_required
        @self._app.route('/load_data_at_startup', methods=["POST"])
        def load_data_at_startup():
            try:
                # self.controller.load_in_data_at_startup()
                current_user.backend_controller.load_in_data_at_startup()
                return jsonify("ACK")
            except:
                return jsonify("NACK")

    def _create_registration_routes(self):
        """:brief Wrapper function to create all functions / flask wrappers + routes for registering a new user"""
        @self._app.route(self.form_sites["registration"], methods=["POST", "GET"])
        def register():
            """ Creates the registration page when this route is triggered"""
            print("in register page")
            # If login not needed, go to homepage
            if current_user.is_authenticated:
                return redirect(self.sites["homepage"])
            print("after authenticated, before register form")
            register_form = user_form_defines.RegistrationForm()
            print(f"Register form = {register_form}")
            
            # Ensure the form is valid, then process it
            if register_form.validate_on_submit():
                print("in on submit")
                username = register_form.username.data
                print("After check username")
                password = register_form.password.data
                self.user_manager.user_manager.add_user(username, password)
                flash(f"Congratulations, user {username} is registered successfully. Please login to continue.")
                return redirect(self.form_sites["login"])
            print("rendering the template")
            # Only gets here if the form is not validated. Restarts the registration process
            return render_template('register_page.html', title='Register', form=register_form, links=self.sites, form_links=self.form_sites)

    def _create_login_routes(self):
        """:brief Wrapper function to create all functions / flask wrappers + routes for logging a user in"""
        @self._app.route(self.form_sites["login"], methods=["POST", "GET"])
        def login():
            if current_user.is_authenticated:
                return redirect(self.sites["homepage"])
            login_form = user_form_defines.LoginForm()
            
            if login_form.validate_on_submit():
                user = self.user_manager.user_manager.get_user_by_username(login_form.username.data)
                if user is None or user.check_password(login_form.password.data) is False:
                    flash('Username or Password is incorrect')
                    return redirect(constants.SITE_PATHS['login'])
                
                # Why this is being done - https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.user_loader
                login_user(user, remember=True)
                return redirect(constants.SITE_PATHS['homepage'])
            # If the user needs to login
            return render_template('login_page.html', title='Sign In', form=login_form, form_links=self.form_sites)

    def _create_task_selection_routes(self):
        """Function responsible for all routes in the Task Selection Panel"""
        @login_required
        @self._app.route('/add_task', methods=['POST'])
        def add_task():
            if request.method == "POST":
                new_task = request.get_json()['new_task']
                # return_code = self.controller.add_task(new_task)
                return_code = current_user.backend_controller.add_task(new_task)

                # Remove lock on dropdown
            return jsonify(return_code)

        @login_required
        @self._app.route('/get_task_list', methods=['POST', 'GET'])
        def get_task_list():
            # task_list = self.controller.get_task_list()
            task_list = current_user.backend_controller.get_task_list()
            self._send_to_client('update_info', {'info': 'Loaded data from previous runs of the program'})
            return jsonify({'task_list': task_list})

    def _create_timer_routes(self):
        """Function responsible for all routes in the timer/Stopwatch Panel"""
        @login_required
        @self._app.route('/start_timer', methods=['POST'])
        def start_timer():
            task_name = request.get_json()['task']
            # self.controller.start_timer(task_name)
            current_user.backend_controller.start_timer(task_name)
            return jsonify('ACK')

        @login_required
        @self._app.route('/stop_timer', methods=['POST'])
        def stop_timer():
            task_name = request.get_json()['task']
            # self.controller.stop_timer(task_name)
            current_user.backend_controller.stop_timer(task_name)
            return jsonify('ACK')

        @login_required
        @self._app.route('/get_current_diff', methods=['POST'])
        def get_current_diff():
            task_name = request.get_json()['task']
            # time_diff = self.controller.get_current_diff(task_name)
            time_diff = current_user.backend_controller.get_current_diff(task_name)

            # units = self.controller.time_units
            units = current_user.backend_controller.time_units
            return jsonify({'time_diff': time_diff, 'units': units})
    
    def _create_time_display_routes(self):
        @login_required
        @self._app.route("/get_total_time", methods=["POST"])
        def get_total_time():
            task_name = request.get_json()['task']
            # total_time = self.controller.get_total_time(task_name)
            total_time = current_user.backend_controller.get_total_time(task_name)

            # units = self.controller.time_units
            units = current_user.backend_controller.time_units
            return jsonify({'total_time': total_time, 'units': units})

        @login_required
        @self._app.route("/get_completed_times", methods=["POST"])
        def get_completed_times():
            task_name = request.get_json()['task']
            # units = self.controller.time_units
            units = current_user.backend_controller.time_units

            # time_list = self.controller.get_completed_time_list(task_name)
            time_list = current_user.backend_controller.get_completed_time_list(task_name)
            return jsonify({'time_list': time_list, 'units': units})

    def _create_url(self):
        # TODO - make port dyanmic and ensure it is unused
        self._host_name = 'localhost'
        self._port = 5000

    def _setup_app_config(self):
        self._cur_file_path = os.path.abspath(os.path.dirname(__file__))
        self._src_root = os.path.dirname(self._cur_file_path)
        self._static_dir = os.path.join(self._src_root, "static")
        self._template_dir = os.path.join(self._src_root, "templates")
        self._images_dir = os.path.join(self._static_dir, "images")
        self._url_root = "Timekeeper"
        self._app = Flask(__name__, 
                    static_folder=self._static_dir, 
                    template_folder=self._template_dir,
                    root_path=self._src_root)
        self._app.config['TEMPLATES_AUTO_RELOAD'] = True

        # Use this to make sure data is kept secure
        self._app.config["SECRET_KEY"] = secrets.token_urlsafe(64)

    def start_app(self):
        """Startup Flask"""
        if self._debug is False:
            self._log = logging.getLogger('werkzeug')
            self._log.setLevel(logging.ERROR)
        else:
            self._log = logging.getLogger('werkzeug')
            self._log.setLevel(logging.INFO)

        # TODO make open only happen when asked via flag
        # webbrowser.open(f"http://{self._host_name}:{self._port}/")

        # Url to go landing_page - http://localhost:5000/about
        landing_page_url = "http://{hostname}:{port}/{landing_page}".format(hostname=self._host_name, 
                                            port=self._port, landing_page=self.sites["landing_page"])
        webbrowser.open(landing_page_url)

        self._app.run(host=self._host_name, port=self._port, debug=self._debug)
        # werkzeug.serving.run_simple(hostname=self._host_name, port=int(self._port), 
        #                         application=self._app, use_debugger=self._debug)