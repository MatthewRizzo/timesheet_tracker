"""File responsible for all flask routes"""
import flask
from flask import request, Flask, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO
import logging
import os
import webbrowser

from backend.backend_controller import BackendController

cur_file_path = os.path.abspath(os.path.dirname(__file__))
src_root = os.path.dirname(cur_file_path)
static_dir = os.path.join(src_root, "static")
template_dir = os.path.join(src_root, "templates")
images_dir = os.path.join(static_dir, "images")
url_root = "Timekeeper"
app = Flask(__name__, 
            static_folder=static_dir, 
            template_folder=template_dir,
            root_path=src_root)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Used to communicate from backend->frontend js
socketio = SocketIO(app, async_mode="threading")

def send_to_client(message_name, content_json=None):
    """Function to enable communication from backend to front-end via sockets"""
    if content_json:
        socketio.emit(message_name, content_json)
    else:
        socketio.emit(message_name)

controller = BackendController(send_to_client)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(images_dir, 'stopwatch.png', mimetype='image/vnd.microsoft.icon')

##########################
# Task Selection Routes  #
##########################
@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == "POST":
        new_task = request.get_json()['new_task']
        return_code = controller.add_task(new_task)
    return jsonify(return_code)

@app.route('/get_task_list', methods=['POST', 'GET'])
def get_task_list():
    task_list = controller.get_task_list()
    
    return jsonify({'task_list': task_list})
    

#################################
# End of Task Selection Routes  #
#################################

#################
# Timer Routes  #
#################
@app.route('/start_timer', methods=['POST'])
def start_timer():
    task_name = request.get_json()['task']
    controller.start_timer(task_name)
    return jsonify('ACK')

@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    task_name = request.get_json()['task']
    controller.stop_timer(task_name)
    return jsonify('ACK')

@app.route('/get_current_diff', methods=['POST'])
def get_current_diff():
    task_name = request.get_json()['task']
    time_diff = controller.get_current_diff(task_name)
    units = controller.time_units
    return jsonify({'time_diff': time_diff, 'units': units})

########################
# End of Timer Routes  #
########################

def start_app():
    # TODO - make port dyanmic and ensure it is unused
    host_name = 'localhost'
    port = 5000
    webbrowser.open(f"http://{host_name}:{port}/")

    debug = False
    if debug is False:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    else:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.INFO)

    app.run(host=host_name, port=port, debug=debug)