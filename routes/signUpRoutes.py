from controllers.signUp import signup

def routeIndex(app):
    app.route('/signup', methods=['POST'])(signup)
    