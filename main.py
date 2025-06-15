from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import db, User
import os

app = Flask(__name__)
app.secret_key = 'figurinapp-secret-key'  # Necessário para usar sessão e flash

# Configuração do banco PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:SUA_SENHA_AQUI@dpg-xxx.oregon-postgres.render.com/figurinapp_xxx'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

# Página inicial (login)
@app.route('/')
def index():
    return render_template('index.html')

# Exibir formulário de cadastro
@app.route('/cadastro', methods=['GET'])
def exibir_cadastro():
    return render_template('cadastro.html')

# Processar cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    if User.query.filter_by(email=email).first():
        flash('Este e-mail já está cadastrado.', 'erro')
        return redirect(url_for('exibir_cadastro'))

    novo_usuario = User(nome=nome, email=email)
    novo_usuario.set_senha(senha)

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'sucesso')
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao cadastrar: {str(e)}"

# Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    usuario = User.query.filter_by(email=email).first()

    if usuario and usuario.check_senha(senha):
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        return redirect(url_for('painel'))
    else:
        flash('E-mail ou senha inválidos.', 'erro')
        return redirect(url_for('index'))

# Painel protegido
@app.route('/painel')
def painel():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    return render_template('painel.html', nome=session['usuario_nome'])

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Testar conexão
@app.route('/testar-banco')
def testar_banco():
    try:
        db.session.execute('SELECT 1')
        return "Banco conectado com sucesso!"
    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
