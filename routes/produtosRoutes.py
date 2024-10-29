from controllers.produtosController import produtosController
from controllers.produtosController import getProdutos

def produtosRoutes(app):
        app.route('/produto', methods=['GET','POST','PUT','DELETE'])(produtosController)
        app.route('/produto/itens', methods=['GET'])(getProdutos) 