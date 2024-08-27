from database.db import db 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Financeiros(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'descricao': self.descricao,
            'idVenda': self.idVenda,
            'isPagarReceber': self.isPagarReceber,
            'valor': self.valor,
            'dataVencimento': self.dataVencimento,
            'dataCompetencia': self.dataCompetencia,
            'dataPagamento': self.dataPagamento,
            'idCliente': self.idCliente,
            'idBanco': self.idBanco,
            'idFormaPgto': self.formaPgto,
            'situacao': self.situacao
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    idVenda = db.Column(ForeignKey('vendas.id'), nullable=False)
    isPagarReceber = db.Column(db.Boolean, nullable=False) #confirmar se é string mesmo
    valor = db.Column(db.Float, nullable=False)
    dataVencimento = db.Column(db.Date, nullable=False)
    dataCompetencia = db.Column(db.Date, nullable=False)
    dataPagamento = db.Column(db.Date, nullable=False)
    idCliente = db.Column(ForeignKey('clientes.id'), nullable=False)
    idBanco = db.Column(ForeignKey('bancos.id'), nullable=False)
    idFormaPgto = db.Column(ForeignKey('forma_pgto.id'), nullable=False)
    situacao = db.Column(db.Integer, nullable=False)

    venda = relationship('Vendas', backref='financeiro')
    cliente = relationship('Clientes', backref='financeiro')
    banco = relationship('Bancos', backref='financeiro')
    forma_pgto = relationship('Forma_pgto', backref='financeiro')

    def __init__(self, descricao, idVenda, isPagarReceber, valor, dataVencimento, dataCompetencia, dataPagamento, idCliente, idBanco, formaPgto, situacao):
        self.descricao = descricao
        self.idVenda = idVenda
        self.isPagarReceber = isPagarReceber
        self.valor = valor
        self.dataVencimento = dataVencimento
        self.dataCompetencia = dataCompetencia
        self.dataPagamento = dataPagamento
        self.idCliente = idCliente
        self.idBanco = idBanco
        self.formaPgto = formaPgto
        self.situacao = situacao
