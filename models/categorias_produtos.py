from database.db import db

class Categorias_produtos(db.Model): #criando representações das tabelas do bancp (db.Model) 
    def to_dict(self): #to_dict transforma database rows em dicioinarios
        return{
            'id': self.id,
            'categoria': self.categoria
        }
    
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    categoria = db.Column(db.String, nullable=False)

    def __init__(self, categoria):
        self.categoria = categoria

