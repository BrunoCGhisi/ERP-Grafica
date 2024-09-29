from controllers.comprasController import comprasController

def comprasRoutes(app):
        app.route('/compra', methods=['GET','POST','PUT','DELETE'])(comprasController)
        