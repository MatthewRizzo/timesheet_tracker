"""File responsible for all flask routes"""
import flask
from flask import request, Flask, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO
import logging
import os
import webbrowser

from backend.backend_controller import BackendController

class AppManager():
    """Class responsible for setting up the Flask app and managing all the routes / sockets"""
    def __init__(self):
        self._setup_app_config()

        # TODO - have this get controlled via an input
        self._debug = False

        # Used to communicate from backend->frontend js
        self._socketio = SocketIO(self._app, async_mode="threading")

        self._create_url()

        self._controller = BackendController(self._send_to_client)

        # Setup App Routes
        self._create_mainpage_routes()
        self._create_task_selection_routes()
        self._create_timer_routes()


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

    def _create_task_selection_routes(self):
        """Function responsible for all routes in the Task Selection Panel"""
        @self._app.route('/add_task', methods=['POST'])
        def add_task():
            if request.method == "POST":
                new_task = request.get_json()['new_task']
                return_code = self._controller.add_task(new_task)
            return jsonify(return_code)

        @self._app.route('/get_task_list', methods=['POST', 'GET'])
        def get_task_list():
            task_list = self._controller.get_task_list()
            
            return jsonify({'task_list': task_list})

    def _create_timer_routes(self):
        """Function responsible for all routes in the timer/Stopwatch Panel"""
        @self._app.route('/start_timer', methods=['POST'])
        def start_timer():
            task_name = request.get_json()['task']
            self._controller.start_timer(task_name)
            return jsonify('ACK')

        @self._app.route('/stop_timer', methods=['POST'])
        def stop_timer():
            task_name = request.get_json()['task']
            self._controller.stop_timer(task_name)
            return jsonify('ACK')

        @self._app.route('/get_current_diff', methods=['POST'])
        def get_current_diff():
            task_name = request.get_json()['task']
            time_diff = self._controller.get_current_diff(task_name)
            units = self._controller.time_units
            return jsonify({'time_diff': time_diff, 'units': units})

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