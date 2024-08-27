from controllers.produtos_categoriasController import produtos_categoriasController

def produtos_categoriasRoutes(app):
        app.route('/produto_categoria', methods=['GET','POST','PUT','DELETE'])(produtos_categoriasController)