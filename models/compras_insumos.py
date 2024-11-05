from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Compras_insumos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'idCompra': self.idCompra, 
            'idInsumo': self.idInsumo,
            'preco': self.preco,
            'tamanho': self.tamanho,
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idCompra = db.Column(ForeignKey("compras.id"), nullable=False)
    idInsumo = db.Column(ForeignKey("insumos.id"), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    tamanho = db.Column(db.Float, nullable=False)

    insumos = relationship('Insumos', backref='compras_insumos')
    compras = relationship('Compras', backref='compras_insumos')

    def __init__(self, idCompra, idInsumo, preco, tamanho):
        self.idCompra = idCompra
        self.idInsumo = idInsumo
        self.preco = preco
        self.tamanho = tamanho
