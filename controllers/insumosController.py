from flask import request
from database.db import db
from models.insumos import Insumos

def getInsumos():
    if request.method == 'GET':
        try:
            insumos = []
            data = Insumos.query.all()
            newData = {'insumos': [insumo.to_dict() for insumo in data]}  # pegando cada obj insumo e transformando em dicionário
            for item in newData['insumos']:
                insumos.append(item)
            
            return insumos, 200
            
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405


def insumosController():

    if request.method == 'POST':
        try:
            data = request.get_json()  # converte em Python
            insumos = Insumos(data['nome'], data['estoque'], data['isActive'])
            db.session.add(insumos)
            db.session.commit()
            return 'Insumos adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405

    elif request.method == 'GET':
        try:
            data = Insumos.query.all()
            newData = {'insumos': [insumo.to_dict() for insumo in data]}  # pegando cada obj insumo e transformando em dicionário
            return newData, 200
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405

    elif request.method == 'PUT':
        try:
            id = request.args.to_dict().get('id')
            insumo = Insumos.query.get(id)
            data = request.get_json()  # pega todos os dados

            if insumo is None:
                return {'error': 'insumo não encontrado'}, 405

            insumo.nome = data.get('nome', insumo.nome)
            insumo.estoque = data.get('estoque', insumo.estoque)
            insumo.isActive = data.get('isActive', insumo.isActive)

            db.session.commit()
            return "insumo atualizado com sucesso", 202

        except Exception as e:
            return f"Não foi possível atualizar o insumo. Erro:{str(e)}", 405

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id')  # pega o id dos dados que o front trouxe
            insumo = Insumos.query.get(id)  # vai procurar insumos no banco com esse id

            if insumo is None:
                return {'error': 'insumo não encontrado'}, 405

            db.session.delete(insumo)
            db.session.commit()
            return "insumo deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o insumo. Erro:{str(e)}", 405
