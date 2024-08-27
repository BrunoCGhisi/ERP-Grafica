from flask import request
from database.db import db
from models.usuarios import Usuarios

def usuariosController():

    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            usuarios = Usuarios(data['nome'], data['email'], data['senha'], data['isAdm'])
            db.session.add(usuarios)
            db.session.commit()
            return 'Usuarios adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        

    elif request.method == 'GET':
        try:
            data = Usuarios.query.all()
            newData = {'usuarios': [usuario.to_dict() for usuario in data]} #pegando cada obj usuario, e tranformando num dicionario
            return newData, 200
        
        except Exception as e:
            return f'Não foi possível buscar. Erro {str(e)}', 405
        

    elif request.method == 'PUT':
            try:
                id = request.args.to_dict().get('id')
                usuario = Usuarios.query.get(id)
                data = request.get_json() #pega todos os dados

                
                if usuario is None:
                    return{'error': 'Usuário não encontrado'}, 405
                
                usuario.nome = data.get('nome', usuario.nome)
                usuario.email = data.get('email', usuario.email)   
                usuario.senha = data.get('senha', usuario.senha)   
                usuario.isAdm = data.get('isAdm', usuario.isAdm)   

                db.session.commit()
                return "Usuário atualizado com sucesso", 202

            except Exception as e:
                return f"Não foi possível atualizar o usuario. Erro:{str(e)}", 405
            

    elif request.method == 'DELETE':
        try:
            id = request.args.to_dict().get('id') #pega o id dos dados que o data trouxe do front
            usuario = Usuarios.query.get(id) # vai procurar usuarios NO BANCO com esse id

            if usuario is None:
                return{'error': 'Usuário não encontrado'}, 405
            
            db.session.delete(usuario)
            db.session.commit()
            return "Usuário deletado com sucesso", 202

        except Exception as e:
            return f"Não foi possível apagar o usuário. Erro:{str(e)}", 405
        

