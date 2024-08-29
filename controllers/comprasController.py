from flask import request
from database.db import db
from models.compras import Compras

def comprasController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            compras = Compras(data['idFornecedor'], data['isCompraOs'], data['dataCompra'], data['numNota'], data['desconto'])

            #IMPLEMENTAR LOGICA IF CLIENTE IS NOT FORNECEDOR IDFORNECEDOR NÃO PODE RECEBER ID 

            db.session.add(compras)
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
                compra.isCompraOs = data.get('isCompraOs', compra.isCompraOs)   
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

            if compra is None:
                return{'error': 'compra não encontrado'}, 405
            
            db.session.delete(compra)
            db.session.commit()
            return "compra deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o compra. Erro:{str(e)}", 405
        

