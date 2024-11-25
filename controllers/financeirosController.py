from flask import request
from database.db import db
from models.financeiros import Financeiros
from models.bancos import Bancos
from models.insumos import Insumos 
from models.produtos import Produtos
from models.vendas_produtos import Vendas_produtos
from datetime import date
from sqlalchemy import func
from flask import jsonify

def getResumoFinanceiro():
    try:
        total_receber = db.session.query(func.sum(Financeiros.valor)).filter_by(isPagarReceber=False).scalar() or 0.0
        total_pagar = db.session.query(func.sum(Financeiros.valor)).filter_by(isPagarReceber=True).scalar() or 0.0

        qtd_contas_receber = db.session.query(func.count(Financeiros.id)).filter_by(isPagarReceber=False).scalar() or 0
        qtd_contas_pagar = db.session.query(func.count(Financeiros.id)).filter_by(isPagarReceber=True).scalar() or 0

        resumo = {
            "totalReceber": total_receber,
            "totalPagar": total_pagar,
            "qtdContasReceber": qtd_contas_receber,
            "qtdContasPagar": qtd_contas_pagar,
        }
        return jsonify(resumo), 200
    except Exception as e:
        return jsonify({"erro": f"Não foi possível calcular o resumo financeiro. Erro: {str(e)}"}), 405

def financeirosController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            financeiros = Financeiros(data['idVenda'], data['idCompra'], data['idBanco'], data['idFormaPgto'], data['descricao'], data['isPagarReceber'], data['valor'], data['dataVencimento'], data['dataCompetencia'], data['dataPagamento'], data['situacao'], data['parcelas'])
            db.session.add(financeiros)
            db.session.commit()
            return 'Financeiros adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Financeiros.query.all()
            newData = [financeiro.to_dict() for financeiro in data] #pegando cada obj financeiro, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                financeiro = Financeiros.query.get(id)
                banco = Bancos.query.get(financeiro.idBanco)
                data = request.get_json() #pega todos os dados

                
                if financeiro is None:
                    return{'error': 'financeiro não encontrado'}, 405
                
               
                financeiro.dataVencimento = data.get('dataVencimento', financeiro.dataVencimento)
                financeiro.dataCompetencia = data.get('dataCompetencia', financeiro.dataCompetencia)       
                
                if financeiro.situacao == 4 and data.get('situacao', financeiro.situacao) == 2:
                    banco.valorTotal -= financeiro.valor
                if financeiro.situacao == 3 and data.get('situacao', financeiro.situacao) == 1:
                    banco.valorTotal += financeiro.valor
                
                financeiro.situacao = data.get('situacao', financeiro.situacao)

                if data.get('situacao', financeiro.situacao) == 4:
                    financeiro.dataPagamento =  date.today()
                    banco.valorTotal += financeiro.valor                

                if data.get('situacao', financeiro.situacao) == 3:
                    banco.valorTotal -= financeiro.valor 
                    financeiro.dataPagamento = date.today()

                db.session.commit()
                return "financeiro atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o financeiro. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            financeiro = Financeiros.query.get(id) # vai procurar financeiros NO BANCO com esse id

            if financeiro is None:
                return{'error': 'financeiro não encontrado'}, 405
            
            db.session.delete(financeiro)
            db.session.commit()
            return "financeiro deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o financeiro. Erro:{str(e)}", 405
        

