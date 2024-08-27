from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Compras_produtos(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'idCompra': self.idCompra, 
            'idProduto': self.idProduto
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idCompra = db.Column(ForeignKey("compras.id"), nullable=False)
    idProduto = db.Column(ForeignKey("produtos.id"), nullable=False)

    produtos = relationship('Produtos', backref='compras_produtos')
    compras = relationship('Compras', backref='compras_produtos')

    def __init__(self, idFornecedor, isCompraOs, dataCompra, numNota):
        self.idFornecedor = idFornecedor
        self.isCompraOs = isCompraOs
        self.dataCompra = dataCompra
        self.numNota = numNota

