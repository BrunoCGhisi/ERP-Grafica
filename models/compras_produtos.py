from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Compras_produtos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'idCompra': self.idCompra, 
            'idProduto': self.idProduto,
            'preco': self.preco,
            'quantidade': self.quantidade,
            'tamanho': self.tamanho,

        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idCompra = db.Column(ForeignKey("compras.id"), nullable=False)
    idProduto = db.Column(ForeignKey("produtos.id"), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tamanho = db.Column(db.Float, nullable=False)

    produtos = relationship('Produtos', backref='compras_produtos')
    compras = relationship('Compras', backref='compras_produtos')

    def __init__(self, idCompra, idProduto, preco, quantidade, tamanho):
        self.idCompra = idCompra
        self.idProduto = idProduto
        self.preco = preco
        self.quantidade = quantidade
        self.tamanho = tamanho
