from controllers.financeirosController import financeirosController, getResumoFinanceiro


def financeirosRoutes(app):
        app.route('/financeiro', methods=['GET','POST','PUT','DELETE'])(financeirosController)
        app.route('/financeiro/resumo', methods=['GET'])(getResumoFinanceiro)
      