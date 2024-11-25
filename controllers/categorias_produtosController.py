from flask import request
from database.db import db
from models.categorias_produtos import Categorias_produtos

def getCategorias():
        if request.method == 'GET':
            try:
                categorias = []
                data = Categorias_produtos.query.all()
                newData = {'Categorias_produtos': [insumo.to_dict() for insumo in data]}  # pegando cada obj insumo e transformando em dicionário
                for item in newData['Categorias_produtos']:
                    categorias.append(item)
                
                return categorias, 200
                
            except Exception as e:
                return f'Não foi possível buscar. Erro {str(e)}', 405

def Categorias_produtosController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            categorias_produtos = Categorias_produtos(data['categoria'], True)
            db.session.add(categorias_produtos)
            db.session.commit()
            return "Categoria adicionada com sucesso!", 200
        except Exception as e:
            return f"Não foi possível inserir. Erro {str(e)}", 405
        

    elif request.method == 'GET':
        try:
            data = Categorias_produtos.query.all()
            newData = []
            catProdAtivos = []
            catProdDesativos = []
            newData = [categoria_produto.to_dict() for categoria_produto in data] #pegando cada obj categoria_produto, e tranformando num dicionario
            catProdAtivos = [i for i in newData if i['isActive']] 
            catProdDesativos = [i for i in newData if not i['isActive']] 
            return {"allData": newData, 'catProdAtivos': catProdAtivos, 'catProdDesativos': catProdDesativos}, 200
        
        except Exception as e:
            return f"Não foi possível buscar. Erro {str(e)}", 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                categoria_produto = Categorias_produtos.query.get(id)
                data = request.get_json() #pega todos os dados

                if categoria_produto is None:
                    return{'error': 'categoria_produto não encontrado'}, 405
                
                categoria_produto.categoria  = data.get('categoria', categoria_produto.categoria )
                categoria_produto.isActive  = data.get('isActive', categoria_produto.categoria )

                db.session.commit()
                return "Categoria atualizada com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar a categoria. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            categoria_produto = Categorias_produtos.query.get(id) # vai procurar Categorias_produtos NO BANCO com esse id

            if categoria_produto is None:
                return{'error': 'categoria_produto não encontrado'}, 405
            
            db.session.delete(categoria_produto)
            db.session.commit()
            return "categoria_produto deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar a categoria. Erro:{str(e)}", 405
        

