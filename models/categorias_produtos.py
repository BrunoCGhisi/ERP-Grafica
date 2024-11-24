from database.db import db

class Categorias_produtos(db.Model): #criando representações das tabelas do bancp (db.Model) 
    def to_dict(self): #to_dict transforma database rows em dicioinarios
        return{
            'id': self.id,
            'categoria': self.categoria,
            'isActive': self.isActive
        }
    
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    categoria = db.Column(db.String, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)

    def __init__(self, categoria, isActive):
        self.categoria = categoria
        self.isActive = isActive


