from controllers.login import login

def loginRoutes(app):
        app.route('/login', methods=['GET','POST'])(login)