"""File responsible for all flask routes"""
import flask
from flask import request, Flask, render_template, send_from_directory
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

controller = BackendController()

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(images_dir, 'stopwatch.png', mimetype='image/vnd.microsoft.icon')

#################
# Timer Routes  #
#################
@app.route('/start_timer')
def start_timer():
    task_name = request.get_json()['task']
    controller.start_timer(task_name)

@app.route('/stop_timer')
def stop_timer():
    task_name = request.get_json()['task']
    controller.stop_timer(task_name)

@app.route('/update_cur_timer')
def update_cur_timer():
    task_name = request.get_json()['task']
    controller.update_cur_timer(task_name)
########################
# End of Timer Routes  #
########################

def start_app():
    # TODO - make port dyanmic and ensure it is unused
    host_name = 'localhost'
    port = 5000
    # webbrowser.open("localhost:5000")
    app.run(host=host_name, port=port, debug=True)