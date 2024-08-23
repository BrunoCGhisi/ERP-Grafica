from controllers.login import login

def loginRoutes(app):
        app.route('/loginho', methods=['GET','POST'])(login)