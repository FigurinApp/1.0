from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__, static_folder='../static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
