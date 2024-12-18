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
            'idInsumo': self.idInsumo,
            'idCategoria': self.idCategoria,
            'largura': self.largura,
            'comprimento': self.comprimento,
            'isActive': self.isActive
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique= True)
    nome = db.Column(db.String(60), nullable=False)
    tipo = db.Column(db.Boolean, nullable=False)
    keyWord = db.Column(db.String, nullable=True)
    idInsumo = db.Column(ForeignKey('insumos.id'), nullable=False)
    idCategoria = db.Column(ForeignKey('categorias_produtos.id'), nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)
    largura = db.Column(db.Float, nullable=False)
    comprimento = db.Column(db.Float, nullable=False)

    categoria = relationship('Categorias_produtos', backref='produtos')
    insumo = relationship('Insumos', backref='produtos')

    def __init__(self, nome, tipo, keyWord, idInsumo, idCategoria, largura, comprimento, isActive):
        self.nome = nome
        self.tipo = tipo
        self.keyWord = keyWord
        self.idInsumo = idInsumo
        self.idCategoria = idCategoria
        self.largura = largura
        self.comprimento = comprimento
        self.isActive = isActive


