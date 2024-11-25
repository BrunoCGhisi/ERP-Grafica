from flask import request, jsonify
from database.db import db
from models.bancos import Bancos
from flask_jwt_extended import jwt_required, get_jwt_identity

def getBancos():
    if request.method == 'GET':
        try:
            bancos = []
            data = Bancos.query.all()
            newData = {'bancos': [banco.to_dict() for banco in data]}  # pegando cada obj banco e transformando em dicionário
            for item in newData['bancos']:
                bancos.append(item)
                print(bancos)
            return bancos, 200
            
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        
def bancosController():
    if request.method == 'POST':
        try:
            data = request.get_json()  # Converte a requisição JSON para Python
            bancos = Bancos(data['nome'], data['valorTotal'], True  )  # Cria o objeto do modelo
            db.session.add(bancos)
            db.session.commit()
            return "Banco adicionado com sucesso!", 200
        except Exception as e:
            return f"Não foi possível inserir. Erro: {str(e)}", 405

    elif request.method == 'GET':
        try:
            data = Bancos.query.all()
            getBancos = []
            getBanco = []
            bancoDesativos = []
            #newData = {'bancos': [banco.to_dict() for banco in data]}  # Transformando para JSON
            getBancos = [banco.to_dict() for banco in data]
            getBanco = [i for i in getBancos if i['isActive']] 
            bancoDesativos = [i for i in getBancos if not i['isActive']] 

            return {
                "allData": getBancos,
                "getBancos": getBanco,
                "bancoDesativos": bancoDesativos
            }, 200
        except Exception as e:
            return f'Não foi possível buscar. Erro: {str(e)}', 405

    elif request.method == 'PUT':
        try:
            id = request.args.get('id')
            banco = Bancos.query.get(id)
            data = request.get_json()  # Pega os dados da requisição

            if banco is None:
                return {'error': 'Banco não encontrado'}, 405

            banco.nome = data.get('nome', banco.nome)
            banco.valorTotal = data.get('valorTotal', banco.valorTotal)
            banco.isActive = data.get('isActive', banco.isActive)

            db.session.commit()
            return "Banco atualizado com sucesso", 202
        except Exception as e:
            return f"Não foi possível atualizar o banco. Erro: {str(e)}", 405

    elif request.method == 'DELETE':
        try:
            id = request.args.get('id')  # Pega o id do banco a ser deletado
            banco = Bancos.query.get(id)

            if banco is None:
                return {'error': 'Banco não encontrado'}, 405

            db.session.delete(banco)
            db.session.commit()
            return "Banco deletado com sucesso", 202
        except Exception as e:
            return f"Não foi possível apagar o banco. Erro: {str(e)}", 405
