from flask import request, jsonify
from models.usuarios import Usuarios
from flask_jwt_extended import create_access_token

def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({"msg": "Email e senha são obrigatórios"}), 400

    # Busca o usuário pelo email
    usuario = Usuarios.query.filter_by(email=data['email']).first()

    # Verifica se o usuário existe e se a senha corresponde ao hash armazenado
    if usuario and usuario.verify_senha(data['senha']):
        # Gera o token JWT com o ID do usuário como identidade
        additional_claims = {"userId": usuario.id, "nome": usuario.nome}
        access_token = create_access_token(identity=usuario.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Credenciais inválidas"}), 401