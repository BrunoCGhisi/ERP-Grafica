from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Compra_produto(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'idCompra': self.idCompra, 
            'idProduto': self.idProduto
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idCompra = db.Column(db.Integer, nullable=False)
    idProduto = db.Column(db.Integer, nullable=False)


    def __init__(self, idFornecedor, isCompraOs, dataCompra, numNota):
        self.idFornecedor = idFornecedor
        self.isCompraOs = isCompraOs
        self.dataCompra = dataCompra
        self.numNota = numNota

