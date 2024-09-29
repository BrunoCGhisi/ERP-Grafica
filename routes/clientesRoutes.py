from controllers.clientesController import clientesController
from controllers.clientesController import getFornecedores

def clientesRoutes(app):
        app.route('/cliente', methods=['GET','POST','PUT','DELETE'])(clientesController)
        app.route('/cliente/fornecedores', methods=['GET'])(getFornecedores)