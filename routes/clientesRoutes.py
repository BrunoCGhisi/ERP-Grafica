from controllers.clientesController import clientesController

def clientesRoutes(app):
        app.route('/cliente', methods=['GET','POST','PUT','DELETE'])(clientesController)