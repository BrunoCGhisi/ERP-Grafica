from controllers.bancosController import bancosController
from controllers.bancosController import getBancos

def bancosRoutes(app):
        app.route('/banco', methods=['GET','POST','PUT','DELETE'])(bancosController)
        app.route('/banco/itens', methods=['GET'])(getBancos) 
