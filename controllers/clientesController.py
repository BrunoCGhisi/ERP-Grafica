from flask import request
from database.db import db
from models.clientes import Clientes

def clientesController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            clientes = Clientes(data['nome'], data['cpfCnpj'], data['email'], data['telefone'], data['isFornecedor'], data['dataCadastro'], data['nomeFantasia'], data['numIe'], data['statusIe'], data['endereco'], data['cep'], data['estado'], data['numero'], data['cidade'], data['complemento'])

            db.session.add(clientes)
            db.session.commit()
            return 'Clientes adicionados com sucesso!', 200
        except Exception as e:  
            return f'Não foi possível inserir. Erro {str(e)}', 405

        

    elif request.method == 'GET':
        try:
            data = Clientes.query.all()
            newData = {'clientes': [cliente.to_dict() for cliente in data]} #pegando cada obj cliente, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                cliente = Clientes.query.get(id)
                data = request.get_json() #pega todos os dados

                
                if cliente is None:
                    return{'error': 'cliente não encontrado'}, 405
                
                cliente.nome = data.get('nome', cliente.nome)
                cliente.nomeFantasia = data.get('nomeFantasia', cliente.nomeFantasia)   
                cliente.cpfCnpj = data.get('cpfCnpj', cliente.cpfCnpj)   
                cliente.email = data.get('email', cliente.email)   
                cliente.telefone = data.get('telefone', cliente.telefone)
                cliente.isFornecedor = data.get('isFornecedor', cliente.isFornecedor)   
                cliente.dataCadastro = data.get('dataCadastro', cliente.dataCadastro)
                cliente.numIe = data.get('numIe', cliente.numIe)   
                cliente.statusIe = data.get('statusIe', cliente.statusIe)   
                cliente.endereco = data.get('endereco', cliente.endereco)
                cliente.cep = data.get('cep', cliente.cep)   
                cliente.estado = data.get('estado', cliente.estado)   
                cliente.numero = data.get('numero', cliente.numero)   
                cliente.cidade = data.get('cidade', cliente.cidade)   
                cliente.complemento = data.get('complemento', cliente.complemento)   

                db.session.commit()
                return "cliente atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o cliente. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            cliente = Clientes.query.get(id) # vai procurar clientes NO BANCO com esse id

            if cliente is None:
                return{'error': 'cliente não encontrado'}, 405
            
            db.session.delete(cliente)
            db.session.commit()
            return "cliente deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o cliente. Erro:{str(e)}", 405
        
