from flask import request
from database.db import db
from models.compras import Compras
from models.compras_produtos import Compras_produtos

def comprasController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            
            #Perguntar pro belone se eu preciso fazer a parte de verificar quem é forncedor no back ou se eu só filtro isso no front-end

            compras = Compras(data['idFornecedor'], data['isCompraOS'], data['dataCompra'], data['numNota'], data['desconto'])
            db.session.add(compras)
            db.session.flush()
            
            dataCompra = data.get('compras_produtos', [])

            for dataC in dataCompra:
                idProduto = dataC['idProduto']
                preco = dataC['preco']
                quantidade = dataC['quantidade']
                tamanho = dataC['tamanho']
                compras_produtos = Compras_produtos(compras.id, idProduto, preco, quantidade, tamanho)
                db.session.add(compras_produtos)

            db.session.commit()
            return 'Compras adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Compras.query.all()
            newData = {'compras': [compra.to_dict() for compra in data]} #pegando cada obj compra, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                compra = Compras.query.get(id)
                data = request.get_json() #pega todos os dados

                
                if compra is None:
                    return{'error': 'compra não encontrado'}, 405
                
                compra.idFornecedor = data.get('idFornecedor', compra.idFornecedor)
                compra.isCompraOS = data.get('isCompraOS', compra.isCompraOS)   
                compra.dataCompra = data.get('dataCompra', compra.dataCompra)   
                compra.numNota = data.get('numNota', compra.numNota)   
                compra.desconto = data.get('desconto', compra.desconto)

                db.session.commit()
                return "compra atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o compra. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            compra = Compras.query.get(id) # vai procurar compras NO BANCO com esse id

            dataCompras_produtos = Compras_produtos.query.all()
            newDataCompras_produtos = {'compras_produtos': [compra_produto.to_dict() for compra_produto in dataCompras_produtos]} #pegando cada obj venda, e tranformando num dicionario
            
            for produto in newDataCompras_produtos['compras_produtos']:
                if int(produto['idCompra']) == int(id):
                    prodObj = Compras_produtos.query.get(produto['id'])
                    db.session.delete(prodObj)


            if compra is None:
                return{'error': 'compra não encontrado'}, 405
            
            db.session.delete(compra)
            db.session.commit()
            return "compra deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o compra. Erro:{str(e)}", 405
        

