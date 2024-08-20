from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Produtos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'tipo': self.tipo, #serviço ou produto
            'keyWord': self.keyWord,
            'idCategoria': self.idCategoria,
            'precoVenda': self.precoVenda, #conferir
            'isEstoque': self.isEstoque,
            'minEstoque': self.minEstoque,
            'estoque': self.estoque
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique= True)
    tipo = db.Column(db.Boolean, nullable=False)
    keyWord = db.Column(db.String)
    idCategoria = db.Column(ForeignKey('produto_categoria.id'))
    precoVenda = db.Column(db.Float, nullable=False)
    isEstoque = db.Column(db.Boolean, nullable=False) #if estoque true, minEstoque e estoque nullable=false
    minEstoque = db.Column(db.Integer)
    estoque = db.Column(db.Float)

    categoria = relationship('Produto_categoria', backref='produtos')

    def __init__(self, tipo, keyWord, idCategoria, precoVenda, isEstoque, minEstoque, estoque):
        self.tipo = tipo
        self.keyWord = keyWord
        self.idCategoria = idCategoria
        self.precoVenda = precoVenda
        self.isEstoque = isEstoque
        self.minEstoque = minEstoque
        self.estoque = estoque

