from flask import request, jsonify
from models.usuarios import Usuarios
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

def login():
    if request.method == 'POST':
        data = request.get_json()
        
        if data is None or 'email' not in data or 'senha' not in data:
            return jsonify({"error": "Dados inválidos"}), 400
        
        email = data.get('email').strip().lower()
        senha = data.get('senha')
        
        if senha is None:
            return jsonify({"error": "Senha não fornecida"}), 400
        
        usuario = Usuarios.query.filter_by(email=email).first()

        if usuario is None:
            return {'error': 'Usuário não encontrado'}, 404
        else:
            if check_password_hash(usuario.senha, str(senha)):
                access_token = create_access_token(identity=usuario.id)
                return jsonify(access_token=access_token), 200
            else:
                return jsonify({"error": "Senha incorreta"}), 401

    else:
        return "Método HTTP inválido", 405
