from flask import request, jsonify
from database.db import db
from models.produtos import Produtos
from sqlalchemy import func
from models.vendas_produtos import Vendas_produtos
from models.produtos import Produtos

def getPieProdutos():
    if request.method == 'GET':
        try:
            produtos = ( 
                db.session.query(
                    Vendas_produtos.idProduto,
                    Produtos.nome,
                    func.sum(Vendas_produtos.quantidade).label('totalVendido')
                )
                .join(Produtos, Vendas_produtos.idProduto == Produtos.id)
                .group_by(Vendas_produtos.idProduto, Produtos.nome)
                .order_by(func.sum(Vendas_produtos.quantidade).desc())
                .limit(5)
                .all()
            )
            produtos_mais_vendidos = [
                {"idProduto": produto.idProduto, "nome": produto.nome, "totalVendido": produto.totalVendido}
                for produto in produtos
            ]
            
            return jsonify(produtos_mais_vendidos), 200
            
        except Exception as e:
            return jsonify({"erro": f"Não foi possível buscar. Erro {str(e)}"}), 405

def getProdutos():
    if request.method == 'GET':
        try:
            produtos = []
            data = Produtos.query.all()
            newData = {'produtos': [produto.to_dict() for produto in data]}  # pegando cada obj produto e transformando em dicionário
            for item in newData['produtos']:
                produtos.append(item)
            return produtos, 200
            
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405

def produtosController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python

            produtos = Produtos(data['nome'], data['tipo'], data['keyWord'], data['idInsumo'], data['idCategoria'], data['preco'], data['largura'], data['comprimento'])
            db.session.add(produtos)
            db.session.commit()
            return 'Produtos adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Produtos.query.all()
            newData = {'produtos': [produto.to_dict() for produto in data]} #pegando cada obj produto, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                produto = Produtos.query.get(id)
                data = request.get_json() #pega todos os dados

                
                if produto is None:
                    return{'error': 'produto não encontrado'}, 405
                
                produto.nome = data.get('nome', produto.nome)
                produto.tipo = data.get('tipo', produto.tipo)
                produto.keyWord = data.get('keyWord', produto.keyWord) 
                produto.idInsumo = data.get('idInsumo', produto.idInsumo)     
                produto.idCategoria = data.get('idCategoria', produto.idCategoria)   
                produto.preco = data.get('preco', produto.preco)
                produto.tamanho = data.get('tamanho', produto.tamanho)
                produto.largura = data.get('largura', produto.largura)    
                produto.comprimento = data.get('comprimento', produto.comprimento)    

                db.session.commit()
                return "produto atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o produto. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            produto = Produtos.query.get(id) # vai procurar produtos NO BANCO com esse id

            if produto is None:
                return{'error': 'produto não encontrado'}, 405
            
            db.session.delete(produto)
            db.session.commit()
            return "produto deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o produto. Erro:{str(e)}", 405
        
