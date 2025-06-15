from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def set_senha(self, senha_plana):
        self.senha = generate_password_hash(senha_plana).decode('utf-8')

    def check_senha(self, senha_plana):
        return check_password_hash(self.senha, senha_plana)
