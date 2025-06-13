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
from database import conectar

@app.route("/testar-banco")
def testar_banco():
    try:
        conn = conectar()
        conn.close()
        return "Conexão com o banco de dados realizada com sucesso!"
    except Exception as e:
        return f"Erro na conexão: {e}"
