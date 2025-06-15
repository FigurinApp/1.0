from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from models import db, User, bcrypt
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuração da conexão com o banco PostgreSQL no Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:5kzDjoQ1FdiaUZfzBVismFY2SFFQuHsl@dpg-d1682numcj7s73bdlp3g-a.oregon-postgres.render.com/figurinapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
bcrypt.init_app(app)

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Página inicial com formulário de login
@app.route('/')
def index():
    return render_template('index.html')

# Exibir o formulário de cadastro (GET)
@app.route('/cadastro', methods=['GET'])
def exibir_cadastro():
    return render_template('cadastro.html')

# Rota para cadastro de usuário (POST)
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    if User.query.filter_by(email=email).first():
        return "Este e-mail já está cadastrado."

    novo_usuario = User(nome=nome, email=email)
    novo_usuario.set_senha(senha)

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao cadastrar usuário: {e}"

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    usuario = User.query.filter_by(email=email).first()

    if usuario and usuario.check_senha(senha):
        return redirect(url_for('index'))  # Futuro: redirecionar para /painel
    else:
        return "Email ou senha inválidos."

# Rota para testar conexão com o banco
@app.route('/testar-banco')
def testar_banco():
    try:
        db.session.execute('SELECT 1')
        return "Conexão com o banco de dados realizada com sucesso!"
    except Exception as e:
        return f"Erro na conexão: {e}"

# Rota para servir arquivos estáticos (como imagens, CSS, etc.)
@app.route('/<path:path>')
def static_proxy(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    return render_template('index.html')

# Execução local
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
