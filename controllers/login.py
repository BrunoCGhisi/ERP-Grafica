from flask import request
from models.usuarios import Usuarios
from werkzeug.security import check_password_hash

def login():
    if request.method == 'POST':
        data = request.get_json()  # Assumindo que os dados são enviados em JSON
        email = data.get('email').strip().lower()
        senha = data.get('senha')
        

        usuario = Usuarios.query.filter_by(email=email).first()

        if usuario is None:
            return{'error': 'Usuário não encontrado'}, 405
        else:
            if check_password_hash(usuario.senha, str(senha)) == True:
                return "Autenticação bem-sucedida"
            else:
                return "Senha incorreta"

    else:
        return "Método HTTP inválido"
    
