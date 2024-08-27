from controllers.vendasController import vendasController

def vendasRoutes(app):
        app.route('/venda', methods=['GET','POST','PUT','DELETE'])(vendasController)