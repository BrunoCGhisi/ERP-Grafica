from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Produtos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo, #serviço ou produto
            'keyWord': self.keyWord,
            'idCategoria': self.idCategoria,
            'preco': self.preco, #conferir
            'tamanho': self.tamanho, #conferir
            'isEstoque': self.isEstoque,
            'minEstoque': self.minEstoque,
            'estoque': self.estoque
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique= True)
    nome = db.Column(db.String(60), nullable=False)
    tipo = db.Column(db.Boolean, nullable=False)
    keyWord = db.Column(db.String, nullable=True)
    idCategoria = db.Column(ForeignKey('categorias_produtos.id'), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    tamanho = db.Column(db.Float, nullable=False)
    isEstoque = db.Column(db.Boolean, nullable=False) #if estoque true, minEstoque e estoque nullable=false
    minEstoque = db.Column(db.Integer, nullable=False)
    estoque = db.Column(db.Float, nullable=False)

    categoria = relationship('Categorias_produtos', backref='produtos')

    def __init__(self, nome, tipo, keyWord, idCategoria, preco, tamanho, isEstoque, minEstoque, estoque):
        self.nome = nome
        self.tipo = tipo
        self.keyWord = keyWord
        self.idCategoria = idCategoria
        self.preco = preco
        self.tamanho = tamanho
        self.isEstoque = isEstoque
        self.minEstoque = minEstoque
        self.estoque = estoque

