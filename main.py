from flask import Flask
from database.db import db 
from routes.routeIndex import routeIndex
from flask_cors import CORS
from flask_jwt_extended import JWTManager  
from datetime import timedelta
    
class MyServer(): #classe que inicializa e guarda o funcionamento do flask
    def __init__(self) -> None:
        self.app = Flask(__name__) #obj de flask que estamos importando
        CORS(self.app)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/artfox' #configurações especificas do ambiente que vamos usar
        self.app.config['JWT_SECRET_KEY'] = 'MinhaKeyCabulosa'  # Chave para JWT
        self.app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
        self.app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=5)
        db.init_app(self.app) #inicializa o flask para usar com a extensão (mysqalchemy )
        routeIndex(self.app) 
        jwt = JWTManager(self.app)
        

    def run(self):
        return self.app.run(port=3000, debug=True, host='localhost')

if __name__ == '__main__' :
    app = MyServer() #instanciando
    app.run() #inicializando
    