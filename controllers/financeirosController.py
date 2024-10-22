from flask import request
from database.db import db
from models.financeiros import Financeiros

def financeirosController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            financeiros = Financeiros(data['descricao'], data['idVenda'], data['isPagarReceber'], data['valor'], data['dataVencimento'], data['dataCompetencia'], data['dataPagamento'], data['idCliente'], data['idFormaPgto'], data['situacao'], data['isOpen'], data['parcelas'])
            db.session.add(financeiros)
            db.session.commit()
            return 'Financeiros adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Financeiros.query.all()
            newData = {'financeiros': [financeiro.to_dict() for financeiro in data]} #pegando cada obj financeiro, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                financeiro = Financeiros.query.get(id)
                data = request.get_json() #pega todos os dados

                
                if financeiro is None:
                    return{'error': 'financeiro não encontrado'}, 405
                
                financeiro.descricao = data.get('descricao', financeiro.descricao)
                financeiro.idVenda = data.get('idVenda', financeiro.idVenda)   
                financeiro.isPagarReceber = data.get('isPagarReceber', financeiro.isPagarReceber)   
                financeiro.valor = data.get('valor', financeiro.valor)   
                financeiro.dataVencimento = data.get('dataVencimento', financeiro.dataVencimento)
                financeiro.dataCompetencia = data.get('dataCompetencia', financeiro.dataCompetencia)   
                financeiro.dataPagamento = data.get('dataPagamento', financeiro.dataPagamento)     
                financeiro.idBanco = data.get('idBanco', financeiro.idBanco)
                financeiro.idFormaPgto = data.get('idFormaPgto', financeiro.idFormaPgto)
                financeiro.situacao = data.get('situacao', financeiro.situacao)
                financeiro.isOpen = data.get('isOpen', financeiro.isOpen)     
                financeiro.parcelas = data.get('parcelas', financeiro.parcelas)  

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
        

