from flask import request
from database.db import db
from flask import request, jsonify
from models.usuarios import Usuarios
from flask_jwt_extended import create_access_token

def signup():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('senha') or not data.get('nome'):
        return jsonify({"msg": "Email, senha e nome são obrigatórios"}), 400

    # Verifica se o usuário já existe
    if Usuarios.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Usuário já existe"}), 400

    # Cria um novo usuário
    novo_usuario = Usuarios(email=data['email'], senha=data['senha'], nome=data['nome'], isAdm=data['isAdm'])
    novo_usuario.set_senha(data['senha'])  # Define a senha hashada
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"msg": "Conta criada com sucesso!"}), 200

# Adicione a nova rota no seu `main.py` ou onde estiver registrando as rotas

