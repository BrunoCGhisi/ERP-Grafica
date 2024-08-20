from database.db import db 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Forma_pgto(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'tipo': self.tipo,
            'idBanco': self.idBanco
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    tipo = db.Column(db.String, nullable=False)
    idBanco = db.Column(ForeignKey('bancos.id'), nullable=False)

    banco = relationship('Bancos', backref='forma_pgto')

    def __init__(self, tipo, idBanco):
        self.tipo = tipo
        self.idBanco = idBanco

