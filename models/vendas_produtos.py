from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Vendas_produtos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'idVenda': self.idVenda, 
            'idProduto': self.idProduto,
            'preco': self.preco,
            'quantidade': self.quantidade,
            'tamanho': self.tamanho,
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idVenda = db.Column(ForeignKey("vendas.id"), nullable=False)
    idProduto = db.Column(ForeignKey("produtos.id"), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tamanho = db.Column(db.Float, nullable=False)

    venda = relationship('Vendas', backref='vendas_produtos')
    produto = relationship('Produtos', backref='vendas_produtos')

    def __init__(self, idVenda, idProduto, preco, quantidade, tamanho):
        self.idVenda = idVenda
        self.idProduto = idProduto
        self.preco = preco
        self.quantidade = quantidade
        self.tamanho = tamanho

