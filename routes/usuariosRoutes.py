from controllers.usuariosController import usuariosController

def usuariosRoutes(app):
        app.route('/usuario', methods=['GET','POST','PUT','DELETE'])(usuariosController)