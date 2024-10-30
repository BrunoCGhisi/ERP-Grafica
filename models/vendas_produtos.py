from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Vendas_produtos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'idVenda': self.idVenda, 
            'idProduto': self.idProduto,
            'quantidade': self.quantidade
        }
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idVenda = db.Column(ForeignKey("vendas.id", ondelete='CASCADE'), nullable=False)
    idProduto = db.Column(ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    venda = relationship('Vendas', backref='vendas_produtos', passive_deletes=True)
    produto = relationship('Produtos', backref='vendas_produtos')

    def __init__(self, idVenda, idProduto, quantidade):
        self.idVenda = idVenda
        self.idProduto = idProduto
        self.quantidade = quantidade


