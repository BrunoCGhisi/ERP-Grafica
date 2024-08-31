from flask import request
from database.db import db
from models.vendas import Vendas
from models.vendas_produtos import Vendas_produtos

def vendasController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            
            vendas = Vendas(data['idCliente'], data['idVendedor'], data['data'], data['isVendaOS'], data['situacao'], data['desconto'])
            
            dataProdutos = data.get('vendas_produtos', [])

            db.session.add(vendas)
            db.session.flush() # para conseguir pegar id
            
            for dataP in dataProdutos:
                idP = dataP['idProduto']
                preco = dataP['preco']
                quantidade = dataP['quantidade']
                tamanho = dataP['tamanho']

                vendas_produtos = Vendas_produtos(vendas.id, idP, preco, quantidade, tamanho)
                db.session.add(vendas_produtos)
            
            db.session.commit()
            return 'Vendas adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            dataVendas = Vendas.query.all()
            dataVendas_produtos = Vendas_produtos.query.all()
            newDataVendas = {'vendas': [venda.to_dict() for venda in dataVendas]}
            newDataVendas_produtos = {'vendas_produtos': [venda_produto.to_dict() for venda_produto in dataVendas_produtos]} #pegando cada obj venda, e tranformando num dicionario

           # datas = [[newDataVendas],[newDataVendas_produtos]]
            data = "ei"

            idVenda = []
            fkVenda = []

            for produto in newDataVendas_produtos['vendas_produtos']:
                fkVenda.append(produto['idVenda']) 

            for venda in newDataVendas['vendas']:
                idVenda.append(venda['id'])

                for item in idVenda:
                    for fk in fkVenda:
                        if fk == item:

                            print(fk, item)

            # for produto in newDataVendas_produtos['vendas_produtos']:
            #     fkVenda.append(produto['id']) 
            # for venda in newDataVendas['vendas']:
            #     idVenda.append(venda['id'])
            #     for idv in idVenda:
            #         item = idVenda[idv]
            #         for fk in fkVenda:
            #             if fkVenda[fk] == item:
            #                 print(fkVenda, item)
                    
            # for i in newDataVendas:
            #     dataDic = newDataVendas[i]
                
            #     for x in dataDic:
            #         idVenda = x['id']

            # print(newDataVendas['vendas'])
                    




            # newDataVendas = {'vendas': [],[]}
            # for venda in dataVendas:
            #     newDataVendas['vendas'].append(venda.to_dict())

          



            
            return data, 200
        
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
        

