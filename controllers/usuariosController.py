from flask import request
from database.db import db
from models.usuarios import Usuarios
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity  # Import JWT requirements

def usuariosController():
        
    if request.method == 'POST':
        try:
            data = request.get_json() # converte em python
            usuarios = Usuarios(data['nome'], data['email'], data['senha'], data['isAdm'], True)
            db.session.add(usuarios)
            db.session.commit()
            return 'Usuarios adicionados com sucesso!', 200
        except Exception as e:
            return f'Não foi possível inserir. Erro {str(e)}', 405
        
    
    elif request.method == 'GET':
        try:
            data = Usuarios.query.all()
            newData = [usuario.to_dict() for usuario in data] #pegando cada obj usuario, e tranformando num dicionario
            usuariosAtivos = [i for i in newData if i['isActive']] 
            usuariosDesativos = [i for i in newData if not i['isActive']] 
            return {'usuariosAtivos': usuariosAtivos, 'usuariosDesativos': usuariosDesativos,
            }, 200
        
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
                usuario.senha = generate_password_hash(data.get('senha'))
                usuario.isAdm = data.get('isAdm', usuario.isAdm) 
                usuario.isActive = data.get('isActive', usuario.isActive)     

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