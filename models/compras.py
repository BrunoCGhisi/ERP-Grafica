from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Compras(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'idFornecedor': self.idFornecedor, #serviço ou produto
            'isCompraOS': self.isCompraOS,
            'dataCompra': self.dataCompra,
            'numNota': self.numNota, #conferir
            'desconto': self.desconto,
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idFornecedor = db.Column(ForeignKey('clientes.id'), nullable=False)
    isCompraOS = db.Column(db.Boolean, nullable=False)
    dataCompra = db.Column(db.String, nullable=False)
    numNota = db.Column(db.Integer, nullable=False)
    desconto = db.Column(db.Integer, nullable=True)

    fornecedor = relationship('Clientes', backref='compras')

    def __init__(self, idFornecedor, isCompraOS, dataCompra, numNota, desconto):
        self.idFornecedor = idFornecedor
        self.isCompraOS = isCompraOS
        self.dataCompra = dataCompra
        self.numNota = numNota
        self.desconto = desconto


