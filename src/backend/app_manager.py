"""File responsible for all flask routes"""
# -- External Packages -- #
import flask
from flask import request, Flask, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO
import logging
import os
import webbrowser

# -- Project Defined Imports -- #
from backend.backend_controller import BackendController

class AppManager():
    """Class responsible for setting up the Flask app and managing all the routes / sockets"""
    def __init__(self):
        self._setup_app_config()

        # TODO - implement a way for users to login. It will change this variable (will have to propoagate to backend as well)
        self._user = "General"

        # TODO - have this get controlled via an input
        self._debug = False

        # Used to communicate from backend->frontend js
        self._socketio = SocketIO(self._app, async_mode="threading")

        self._create_url()

        self.controller = BackendController(self._send_to_client, self._user)

        # Setup App Routes
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
        @self._app.route("/")
        def homepage():
            return render_template("index.html")

        @self._app.route('/favicon.ico')
        def favicon():
            return send_from_directory(self._images_dir, 'stopwatch.png', mimetype='image/vnd.microsoft.icon')

        @self._app.route("/load_data_at_startup", methods=["POST"])
        def load_data_at_startup():
            try:
                self.controller.load_in_data_at_startup()
                return jsonify("ACK")
            except:
                return jsonify("NACK")

    def _create_task_selection_routes(self):
        """Function responsible for all routes in the Task Selection Panel"""
        @self._app.route('/add_task', methods=['POST'])
        def add_task():
            if request.method == "POST":
                new_task = request.get_json()['new_task']
                return_code = self.controller.add_task(new_task)

                # Remove lock on dropdown
            return jsonify(return_code)

        @self._app.route('/get_task_list', methods=['POST', 'GET'])
        def get_task_list():
            task_list = self.controller.get_task_list()
            self._send_to_client('update_info', {'info': 'Loaded data from previous runs of the program'})
            return jsonify({'task_list': task_list})

    def _create_timer_routes(self):
        """Function responsible for all routes in the timer/Stopwatch Panel"""
        @self._app.route('/start_timer', methods=['POST'])
        def start_timer():
            task_name = request.get_json()['task']
            self.controller.start_timer(task_name)
            return jsonify('ACK')

        @self._app.route('/stop_timer', methods=['POST'])
        def stop_timer():
            task_name = request.get_json()['task']
            self.controller.stop_timer(task_name)
            return jsonify('ACK')

        @self._app.route('/get_current_diff', methods=['POST'])
        def get_current_diff():
            task_name = request.get_json()['task']
            time_diff = self.controller.get_current_diff(task_name)
            units = self.controller.time_units
            return jsonify({'time_diff': time_diff, 'units': units})
    
    def _create_time_display_routes(self):
        @self._app.route("/get_total_time", methods=["POST"])
        def get_total_time():
            task_name = request.get_json()['task']
            total_time = self.controller.get_total_time(task_name)
            units = self.controller.time_units
            return jsonify({'total_time': total_time, 'units': units})

        @self._app.route("/get_completed_times", methods=["POST"])
        def get_completed_times():
            task_name = request.get_json()['task']
            units = self.controller.time_units
            time_list = self.controller.get_completed_time_list(task_name)
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

    def start_app(self):
        """Startup Flask"""
        if self._debug is False:
            self._log = logging.getLogger('werkzeug')
            self._log.setLevel(logging.ERROR)
        else:
            self._log = logging.getLogger('werkzeug')
            self._log.setLevel(logging.INFO)

        webbrowser.open(f"http://{self._host_name}:{self._port}/")
        self._app.run(host=self._host_name, port=self._port, debug=self._debug)