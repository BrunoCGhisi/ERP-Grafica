from controllers.insumosController import insumosController
from controllers.insumosController import getInsumos

def insumosRoutes(app):
        app.route('/insumo', methods=['GET','POST','PUT','DELETE'])(insumosController)
        app.route('/insumo/itens', methods=['GET'])(getInsumos) 