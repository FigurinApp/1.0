from flask import Flask, send_from_directory, render_template
from database import conectar
from models import db
import os

app = Flask(__name__, static_folder='../static', template_folder='templates')

# Configuração do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:5kzDjoQ1FdiaUZfzBVismFY2SFFQuHsl@dpg-d1682numcj7s73bdlp3g-a.oregon-postgres.render.com/figurinapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o banco com a aplicação
db.init_app(app)

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

# Criar as tabelas automaticamente ao iniciar
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
