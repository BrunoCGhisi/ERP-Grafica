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
            'idFormaPgto': self.idFormaPgto,
            'situacao': self.situacao,
            'isOpen': self.isOpen,
            'parcelas': self.parcelas
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    idVenda = db.Column(ForeignKey('vendas.id'), nullable=False)
    isPagarReceber = db.Column(db.Boolean, nullable=False) #confirmar se é string mesmo
    valor = db.Column(db.Float, nullable=False)
    dataVencimento = db.Column(db.Date, nullable=False)
    dataCompetencia = db.Column(db.Date, nullable=False)
    dataPagamento = db.Column(db.Date, nullable=True)
    idFormaPgto = db.Column(ForeignKey('formas_pgto.id'), nullable=False)
    situacao = db.Column(db.Integer, nullable=False)
    parcelas = db.Column(db.Integer, nullable=False)
    isOpen = db.Column(db.Boolean, nullable=True)

    venda = relationship('Vendas', backref='financeiros')
    forma_pgto = relationship('Formas_pgto', backref='financeiros')

    def __init__(self, descricao, idVenda, isPagarReceber, valor, dataVencimento, dataCompetencia, dataPagamento, idFormaPgto, situacao, isOpen, parcelas):
        self.descricao = descricao
        self.idVenda = idVenda
        self.isPagarReceber = isPagarReceber
        self.valor = valor
        self.dataVencimento = dataVencimento
        self.dataCompetencia = dataCompetencia
        self.dataPagamento = dataPagamento
        self.idFormaPgto = idFormaPgto
        self.situacao = situacao
        self.isOpen = isOpen
        self.parcelas = parcelas
