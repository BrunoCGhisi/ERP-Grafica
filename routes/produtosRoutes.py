from controllers.produtosController import produtosController

def produtosRoutes(app):
        app.route('/produto', methods=['GET','POST','PUT','DELETE'])(produtosController)