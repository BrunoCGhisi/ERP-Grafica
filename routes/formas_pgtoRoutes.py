from controllers.formas_pgtoController import formas_pgtoController

def formas_pgtoRoutes(app):
        app.route('/formas_pgto', methods=['GET','POST','PUT','DELETE'])(formas_pgtoController)