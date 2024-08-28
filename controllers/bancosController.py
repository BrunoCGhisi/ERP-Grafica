from flask import request
from database.db import db
from models.bancos import Bancos

def bancosController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            bancos = Bancos(data['nome'], data['valorTotal'])
            db.session.add(bancos)
            db.session.commit()
            return "Bancos adicionados com sucesso!", 200
        except Exception as e:
            return f"Não foi possível inserir. Erro {str(e)}", 405
        

    elif request.method == 'GET':
        try:
            data = Bancos.query.all()
            newData = {'bancos': [banco.to_dict() for banco in data]} #pegando cada obj banco, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                print("id", id)
                banco = Bancos.query.get(id)
                data = request.get_json() #pega todos os dados
                print(banco)
                if banco is None:
                    return{'error': 'Banco não encontrado'}, 405
                
                banco.nome = data.get('nome', banco.nome)
                banco.valorTotal = data.get('valorTotal', banco.valorTotal)   

                db.session.commit()
                return "Banco atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o banco. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            banco = Bancos.query.get(id) # vai procurar bancos NO BANCO com esse id

            if banco is None:
                return{'error': 'Banco não encontrado'}, 405
            
            db.session.delete(banco)
            db.session.commit()
            return "Banco deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o banco. Erro:{str(e)}", 405
        

