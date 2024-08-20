from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Vendas(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'idCliente': self.idCliente, #serviço ou produto
            'idVendedor': self.idVendedor,
            'data': self.data,
            'isVendaOs': self.isVendaOs, #conferir
            'situacao': self.situacao,
            'totalVenda': self.totalVenda, #conferir
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idCliente = db.Column(ForeignKey('clientes.id'), nullable=False)
    idVendedor = db.Column(ForeignKey('usuarios.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    isVendaOs = db.Column(db.Integer, nullable=False)
    situacao = db.Column(db.Date, nullable=False)
    totalVenda = db.Column(db.Integer, nullable=False)

    cliente = relationship('Clientes', backref='vendas')
    usuario = relationship('Usuarios', backref='vendas')

    def __init__(self, idCliente, idVendedor, data, isVendaOs, situacao, totalVenda):
        self.idCliente = idCliente
        self.idVendedor = idVendedor
        self.data = data
        self.isVendaOs = isVendaOs
        self.situacao = situacao
        self.totalVenda = totalVenda

