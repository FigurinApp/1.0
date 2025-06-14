from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bcrypt import Bcrypt
from database import conectar
from models import User
import os

app = Flask(__name__, static_folder='../static', template_folder='templates')
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    return render_template('index.html')

@app.route('/testar-banco')
def testar_banco():
    try:
        conn = conectar()
        conn.close()
        return "Conexão com o banco de dados realizada com sucesso!"
    except Exception as e:
        return f"Erro na conexão: {e}"

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    
    senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)",
            (nome, email, senha_hash)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao cadastrar usuário: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
