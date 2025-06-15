from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import os

# Inicialização do app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'minha_chave_secreta'  # Necessária para usar flash

# Configuração do banco de dados PostgreSQL no Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:5kzDjoQ1FdiaUZfzBVismFY2SFFQuHsl@dpg-d1682numcj7s73bdlp3g-a.oregon-postgres.render.com/figurinapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
bcrypt = Bcrypt(app)

# Criar tabelas no banco
with app.app_context():
    db.create_all()

# Página inicial - Login
@app.route('/')
def index():
    return render_template('index.html')

# Página de cadastro (GET e POST)
@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado. Tente outro.")
            return redirect(url_for("cadastro"))

        senha_criptografada = generate_password_hash(senha)
        novo_usuario = User(nome=nome, email=email, senha=senha_criptografada)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Usuário cadastrado com sucesso!")
            return redirect(url_for('index'))
        except Exception as e:
            return f"Erro ao cadastrar usuário: {e}"

    return render_template("cadastro.html")

# Rota de login (POST)
@app.route('/login', methods=["POST"])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = User.query.filter_by(email=email).first()

    if usuario and check_password_hash(usuario.senha, senha):
        flash("Login realizado com sucesso!")
        return redirect(url_for('index'))  # Pode mudar futuramente para painel
    else:
        flash("E-mail ou senha inválidos.")
        return redirect(url_for('index'))

# Rota para arquivos estáticos (Render workaround)
@app.route('/<path:path>')
def static_proxy(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    return render_template('index.html')

# Rota para testar banco
@app.route('/testar-banco')
def testar_banco():
    try:
        db.session.execute('SELECT 1')
        return "Conexão com o banco de dados realizada com sucesso!"
    except Exception as e:
        return f"Erro na conexão: {e}"

# Execução local
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
