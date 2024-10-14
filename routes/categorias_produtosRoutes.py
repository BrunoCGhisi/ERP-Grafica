from controllers.categorias_produtosController import Categorias_produtosController
from controllers.categorias_produtosController import getCategorias


def categorias_produtosRoutes(app):
        app.route('/categoria_produto', methods=['GET','POST','PUT','DELETE'])(Categorias_produtosController)
        app.route('/categoria_produto/itens', methods=['GET'])(getCategorias)