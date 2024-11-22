from database.db import db 

class Insumos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'estoque': self.estoque,
            'isActive': self.isActive,
            'valorM2': self.valorM2,
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    nome = db.Column(db.String, nullable=False)
    estoque = db.Column(db.Float, nullable=False)
    valorM2 = db.Column(db.Float, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)

    def __init__(self, nome, estoque, isActive, valorM2):
        self.nome = nome
        self.estoque = estoque
        self.isActive = isActive
        self.valorM2 = valorM2

