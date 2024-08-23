from routes.usuariosRoutes import usuariosRoutes
from routes.loginRoutes import loginRoutes

def routeIndex(app):
    usuariosRoutes(app)
    loginRoutes(app)