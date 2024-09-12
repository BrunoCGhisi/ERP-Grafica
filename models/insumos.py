from database.db import db 

class Insumo(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'estoque': self.estoque
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    nome = db.Column(db.String, nullable=False)
    estoque = db.Column(db.Float, nullable=False)

    def __init__(self, nome, estoque):
        self.nome = nome
        self.estoque = estoque

