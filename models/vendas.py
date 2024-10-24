from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Vendas(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'idCliente': self.idCliente, #serviço ou produto
            'idVendedor': self.idVendedor,
            'dataAtual': self.dataAtual,
            'isVendaOS': self.isVendaOS, #conferir
            'situacao': self.situacao,
            'desconto': self.desconto #conferir
        }
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idCliente = db.Column(ForeignKey('clientes.id'), nullable=False)
    idVendedor = db.Column(ForeignKey('usuarios.id'), nullable=False)
    dataAtual = db.Column(db.String, nullable=False)
    isVendaOS = db.Column(db.Integer, nullable=False)
    situacao = db.Column(db.Integer, nullable=False)
    desconto = db.Column(db.Integer, nullable=True)

    cliente = relationship('Clientes', backref='vendas')
    usuario = relationship('Usuarios', backref='vendas')

    def __init__(self, idCliente, idVendedor, dataAtual, isVendaOS, situacao, desconto):
        self.idCliente = idCliente
        self.idVendedor = idVendedor
        self.dataAtual = dataAtual
        self.isVendaOS = isVendaOS
        self.situacao = situacao
        self.desconto = desconto

