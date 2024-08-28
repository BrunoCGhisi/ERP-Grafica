from controllers.categorias_produtosController import Categorias_produtosController

def categorias_produtosRoutes(app):
        app.route('/categoria_produto', methods=['GET','POST','PUT','DELETE'])(Categorias_produtosController)