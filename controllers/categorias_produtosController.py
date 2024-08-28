from flask import request
from database.db import db
from models.categorias_produtos import Categorias_produtos

def Categorias_produtosController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            categorias_produtos = Categorias_produtos(data['categoria'])
            db.session.add(categorias_produtos)
            db.session.commit()
            return 'Categorias_produtos adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Categorias_produtos.query.all()
            newData = {'categorias_produtos': [categoria_produto.to_dict() for categoria_produto in data]} #pegando cada obj categoria_produto, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                categoria_produto = Categorias_produtos.query.get(id)
                data = request.get_json() #pega todos os dados

                if categoria_produto is None:
                    return{'error': 'categoria_produto não encontrado'}, 405
                
                categoria_produto.nome = data.get('categoria', categoria_produto.nome)

                db.session.commit()
                return "categoria_produto atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o categoria_produto. Erro:{str(e)}", 405
            

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
            return f"Não foi possível apagar o categoria_produto. Erro:{str(e)}", 405
        

