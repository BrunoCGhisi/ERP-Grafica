from database.db import db 

class Bancos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'valorTotal': self.valorTotal,
            'isActive': self.isActive,
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    nome = db.Column(db.String, nullable=False)
    valorTotal = db.Column(db.String, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)

    def __init__(self, nome, valorTotal, isActive):
        self.nome = nome
        self.valorTotal = valorTotal
        self.isActive = isActive

