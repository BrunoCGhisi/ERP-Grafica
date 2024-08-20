from database.db import db 

class Bancos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'valorTotal': self.valorTotal
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    nome = db.Column(db.String, nullable=False)
    valorTotal = db.Column(db.String, nullable=False)

    def __init__(self, nome, valorTotal):
        self.nome = nome
        self.valorTotal = valorTotal

