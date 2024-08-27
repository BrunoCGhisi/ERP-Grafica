from controllers.bancosController import bancosController

def bancosRoutes(app):
        app.route('/banco', methods=['GET','POST','PUT','DELETE'])(bancosController)