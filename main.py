from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, bcrypt, User

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura_do_figurinapp'

# ✅ Conexão com o banco PostgreSQL do Render — COM SSL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:5kzDjoQ1FdiaUZfzBVismFY2SFFQuHsl@dpg-d1682numcj7s73bdlp3g-a.oregon-postgres.render.com/figurinapp?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar banco e criptografia
db.init_app(app)
bcrypt.init_app(app)

# Criar tabelas se ainda não existirem
with app.app_context():
    db.create_all()

# Página de login
@app.route('/')
def index():
    return render_template('index.html')

# Página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Processar cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    if User.query.filter_by(email=email).first():
        flash('E-mail já cadastrado. Faça login ou use outro.')
        return redirect(url_for('cadastro'))

    novo_usuario = User(nome=nome, email=email)
    novo_usuario.set_senha(senha)

    db.session.add(novo_usuario)
    db.session.commit()

    flash('Cadastro realizado com sucesso! Faça login.')
    return redirect(url_for('index'))

# Processar login (opcional)
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    usuario = User.query.filter_by(email=email).first()
    if usuario and usuario.check_senha(senha):
        flash(f'Bem-vindo(a), {usuario.nome}!')
        return redirect(url_for('index'))
    else:
        flash('E-mail ou senha inválidos.')
        return redirect(url_for('index'))

# Rodar localmente
if __name__ == '__main__':
    app.run(debug=True)
