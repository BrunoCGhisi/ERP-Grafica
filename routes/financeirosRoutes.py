from controllers.financeirosController import financeirosController

def financeirosRoutes(app):
        app.route('/financeiro', methods=['GET','POST','PUT','DELETE'])(financeirosController)