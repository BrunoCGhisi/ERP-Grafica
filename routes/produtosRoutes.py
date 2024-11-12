from controllers.produtosController import produtosController
from controllers.produtosController import getProdutos
from controllers.produtosController import getPieProdutos

def produtosRoutes(app):
        app.route('/produto', methods=['GET','POST','PUT','DELETE'])(produtosController)
        app.route('/produto/itens', methods=['GET'])(getProdutos) 
        app.route('/produto/PieVendidos', methods=['GET'])(getPieProdutos)