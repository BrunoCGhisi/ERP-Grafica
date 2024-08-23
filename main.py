from flask import Flask
from database.db import db 
from routes.routeIndex import routeIndex
from flask_cors import CORS


class MyServer(): #classe que inicializa e guarda o funcionamento do flask
    def __init__(self) -> None:
        self.app = Flask(__name__) #obj de flask que estamos importando
        CORS(self.app)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/artfox' #configurações especificas do ambiente que vamos usar
        db.init_app(self.app) #inicializa o flask para usar com a extensão (mysqalchemy )
        routeIndex(self.app) 

    def run(self):
        return self.app.run(port=3000, debug=True, host='localhost')

if __name__ == '__main__' :
    app = MyServer() #instanciando
    app.run() #inicializando