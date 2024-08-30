from flask import request
from database.db import db
from models.vendas import Vendas
from models.vendas_produtos import Vendas_produtos

def vendasController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            
            vendas = Vendas(data['idCliente'], data['idVendedor'], data['data'], data['isVendaOS'], data['situacao'], data['totalVenda'], data['desconto'])
            
            dataProdutos = data.get('vendas_produtos', [])

            db.session.add(vendas)
            db.session.flush() # para conseguir pegar id
            
            for dataP in dataProdutos:
                idP = dataP['idProduto']
                preco = dataP['preco']
                quantidade = dataP['quantidade']
                tamanho = dataP['tamanho']
                print(preco)

                vendas_produtos = Vendas_produtos(vendas.id, idP, preco, quantidade, tamanho)
                db.session.add(vendas_produtos)
           
            
            
            
            db.session.commit()
            return 'Vendas adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Vendas.query.all()
            newData = {'vendas': [venda.to_dict() for venda in data]} #pegando cada obj venda, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                venda = Vendas.query.get(id)
                data = request.get_json() #pega todos os dados

                
                if venda is None:
                    return{'error': 'venda não encontrado'}, 405
                
                venda.idCliente = data.get('idCliente', venda.idCliente)
                venda.idVendedor = data.get('idVendedor', venda.idVendedor)   
                venda.data = data.get('data', venda.data)   
                venda.isVendaOS = data.get('isVendaOS', venda.isVendaOs)   
                venda.situacao = data.get('situacao', venda.situacao)
                venda.totalVenda = data.get('totalVenda', venda.totalVenda)   
                venda.desconto = data.get('desconto', venda.desconto)

                db.session.commit()
                return "venda atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o venda. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            venda = Vendas.query.get(id) # vai procurar vendas NO BANCO com esse id

            if venda is None:
                return{'error': 'venda não encontrado'}, 405
            
            db.session.delete(venda)
            db.session.commit()
            return "venda deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o venda. Erro:{str(e)}", 405
        

