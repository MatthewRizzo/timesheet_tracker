import flask
from flask import request, Flask, render_template, send_from_directory
import os
import webbrowser

cur_file_path = os.path.abspath(os.path.dirname(__file__))
src_root = os.path.dirname(cur_file_path)
static_dir = os.path.join(src_root, "static")
template_dir = os.path.join(src_root, "templates")
images_dir = os.path.join(static_dir, "images")
print(f"static_dir={static_dir}")
url_root = "Timekeeper"
app = Flask(__name__, 
            static_folder=static_dir, 
            template_folder=template_dir,
            root_path=src_root)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(images_dir, 'stopwatch.png', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    # TODO - make port dyanmic and ensure it is unused
    host_name = 'localhost'
    port = 5000
    # webbrowser.open("localhost:5000")
    app.run(host=host_name, port=port, debug=True)
