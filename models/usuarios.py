from database.db import db 

class Usuarios(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'isAdm': self.isAdm
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    senha = db.Column(db.String, nullable=False)
    isAdm = db.Column(db.String, nullable=False)

    def __init__(self, nome, email, senha, isAdm):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.isAdm = isAdm
        
