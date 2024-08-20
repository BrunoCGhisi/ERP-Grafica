from database.db import db 

class Clientes(db.Model):
    def to_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'nomeFantasia': self.nomeFantasia,
            'cpfCnpj': self.cpfCnpj,
            'email': self.email,
            'telefone': self.telefone,
            'isFornecedor': self.isFornecedor,
            'cadastroData': self.cadastroData,
            'numIe': self.numIe,
            'statusIe': self.statusIe,
            'endereco': self.endereco,
            'cep': self.cep,
            'estado': self.estado,
            'numero': self.numero,
            'cidade': self.cidade,
            'complemento': self.complemento
            }

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    nome = db.Column(db.String, nullable=False)
    nomeFantasia = db.Column(db.String)
    cpfCnpj = db.Column(db.String, nullable=False) #confirmar se é string mesmo
    email = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    isFornecedor = db.Column(db.Boolean, nullable=False)
    cadastroData = db.Column(db.Date, nullable=False)
    numIe = db.Column(db.Integer)
    statusIe = db.Column(db.Integer)
    endereco = db.Column(db.String)
    cep = db.Column(db.Integer)
    estado = db.Column(db.String)
    numero = db.Column(db.Integer)
    cidade = db.Column(db.String)
    complemento = db.Column(db.String)

    def __init__(self, nome, nomeFantasia, cpfCnpj, email, telefone, isFornecedor, cadastroData, numIe, statusIe, endereco, cep, estado, numero, cidade, complemento):
        self.nome = nome
        self.nomeFantasia = nomeFantasia
        self.cpfCnpj = cpfCnpj
        self.email = email
        self.telefone = telefone
        self.isFornecedor = isFornecedor
        self.cadastroData = cadastroData
        self.numIe = numIe
        self.statusIe = statusIe
        self.endereco = endereco
        self.cep = cep
        self.estado = estado
        self.numero = numero
        self.cidade = cidade
        self.complemento = complemento
