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
            'dataCadastro': self.dataCadastro,
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
    nomeFantasia = db.Column(db.String, nullable=True)
    cpfCnpj = db.Column(db.String, nullable=False) #confirmar se é string mesmo
    email = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    isFornecedor = db.Column(db.Boolean, nullable=False)
    dataCadastro = db.Column(db.Date, nullable=False)
    numIe = db.Column(db.Integer, nullable=True)
    statusIe = db.Column(db.Boolean, nullable=True)
    endereco = db.Column(db.String, nullable=True)
    cep = db.Column(db.Integer, nullable=True)
    estado = db.Column(db.String, nullable=True)
    numero = db.Column(db.Integer, nullable=True)
    cidade = db.Column(db.String, nullable=True)
    complemento = db.Column(db.String, nullable=True)

    def __init__(self, nome, cpfCnpj, email, telefone, isFornecedor, dataCadastro, nomeFantasia, numIe, statusIe, endereco, cep, estado, numero, cidade, complemento):
        self.nome = nome
        self.cpfCnpj = cpfCnpj
        self.email = email
        self.telefone = telefone
        self.isFornecedor = isFornecedor
        self.dataCadastro = dataCadastro
        self.nomeFantasia = nomeFantasia
        self.numIe = numIe
        self.statusIe = statusIe
        self.endereco = endereco
        self.cep = cep
        self.estado = estado
        self.numero = numero
        self.cidade = cidade
        self.complemento = complemento
