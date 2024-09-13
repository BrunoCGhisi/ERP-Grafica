from routes.usuariosRoutes import usuariosRoutes
from routes.loginRoutes import loginRoutes
from routes.bancosRoutes import bancosRoutes
from routes.clientesRoutes import clientesRoutes
from routes.comprasRoutes import comprasRoutes
from routes.financeirosRoutes import financeirosRoutes
from routes.formas_pgtoRoutes import formas_pgtoRoutes
from routes.categorias_produtosRoutes import categorias_produtosRoutes
from routes.produtosRoutes import produtosRoutes
from routes.vendasRoutes import vendasRoutes
from routes.insumosRoutes import insumosRoutes

def routeIndex(app):
    usuariosRoutes(app)
    loginRoutes(app)
    bancosRoutes(app)
    clientesRoutes(app)
    comprasRoutes(app)
    financeirosRoutes(app)
    formas_pgtoRoutes(app)
    categorias_produtosRoutes(app)
    produtosRoutes(app)
    vendasRoutes(app)
    insumosRoutes(app)