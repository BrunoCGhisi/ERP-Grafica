from database.db import db 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Formas_pgto(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'tipo': self.tipo,
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    tipo = db.Column(db.String, nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo


