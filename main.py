from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, bcrypt, User
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'

# Banco de dados PostgreSQL do Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:94lJQwUuE5ljec1kegGiCz2YhA6sOY4J@dpg-d1682numcj7s73bdlp3g-a.oregon-postgres.render.com/figurinapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    usuario_existente = User.query.filter_by(email=email).first()
    if usuario_existente:
        flash('E-mail já cadastrado. Faça login ou use outro e-mail.')
        return redirect(url_for('cadastro'))

    novo_usuario = User(nome=nome, email=email)
    novo_usuario.set_senha(senha)

    db.session.add(novo_usuario)
    db.session.commit()

    flash('Usuário cadastrado com sucesso! Faça login.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
