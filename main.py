from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User
import os

app = Flask(__name__)
app.secret_key = 'figurinapp-secret-key'  # Necessário para flash() e login

# Config do banco PostgreSQL (Render)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:dFY4vaX6yNog0BLJk3yulfzmfFToMVmK@dpg-d17f842dbo4c73fsdm8g-a.oregon-postgres.render.com/figurinapp_7k03'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

# Config login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET'])
def exibir_cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.')
            return redirect(url_for('exibir_cadastro'))

        novo_usuario = User(nome=nome, email=email)
        novo_usuario.set_senha(senha)

        db.session.add(novo_usuario)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('index'))

    except Exception as e:
        return f"Erro ao cadastrar: {str(e)}"

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    usuario = User.query.filter_by(email=email).first()

    if usuario and usuario.check_senha(senha):
        login_user(usuario)
        return redirect(url_for('painel'))
    else:
        flash('E-mail ou senha inválidos.')
        return redirect(url_for('index'))

@app.route('/painel')
@login_required
def painel():
    return render_template('painel/painel.html', usuario=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/testar-banco')
def testar_banco():
    try:
        db.session.execute('SELECT 1')
        return "Banco conectado com sucesso!"
    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
