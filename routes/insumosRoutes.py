from controllers.insumosController import insumosController

def insumosRoutes(app):
        app.route('/insumo', methods=['GET','POST','PUT','DELETE'])(insumosController)