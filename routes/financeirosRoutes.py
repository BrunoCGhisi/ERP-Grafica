from controllers.financeirosController import financeirosController, getResumoFinanceiro, vendasDoMesAtual


def financeirosRoutes(app):
        app.route('/financeiro', methods=['GET','POST','PUT','DELETE'])(financeirosController)
        app.route('/financeiro/resumo', methods=['GET'])(getResumoFinanceiro)
        app.route('/vendas/mensais', methods=['GET'])(vendasDoMesAtual)
      