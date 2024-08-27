from flask import request
from database.db import db
from models.produtos_categorias import Produtos_categorias

def produtos_categoriasController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            produtos_categorias = Produtos_categorias(data['categoria'])
            db.session.add(produtos_categorias)
            db.session.commit()
            return 'Produtos_categorias adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Produtos_categorias.query.all()
            newData = {'produtos_categorias': [produto_categoria.to_dict() for produto_categoria in data]} #pegando cada obj produto_categoria, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                produto_categoria = Produtos_categorias.query.get(id)
                data = request.get_json() #pega todos os dados

                if produto_categoria is None:
                    return{'error': 'Produto_categoria não encontrado'}, 405
                
                produto_categoria.nome = data.get('categoria', produto_categoria.nome)

                db.session.commit()
                return "Produto_categoria atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o produto_categoria. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            produto_categoria = Produtos_categorias.query.get(id) # vai procurar produtos_categorias NO BANCO com esse id

            if produto_categoria is None:
                return{'error': 'Produto_categoria não encontrado'}, 405
            
            db.session.delete(produto_categoria)
            db.session.commit()
            return "Produto_categoria deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o produto_categoria. Erro:{str(e)}", 405
        

