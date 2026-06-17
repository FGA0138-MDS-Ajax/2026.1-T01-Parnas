from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.user_service import delete_user, register_user, update_user
from app.schemas.user_schema import UserRegistrationSchema, UserRequirements
from marshmallow import ValidationError
from flask import render_template

user_bp = Blueprint("user_bp", __name__)

user_schema = UserRegistrationSchema()
user_response_schema = UserRequirements()

@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = user_schema.load(request.get_json())
        if not data:
            return jsonify({"erro": "Nenhum JSON recebido"}), 400
    except ValidationError as err:
        return jsonify({"erros_de_validcao": err.messages}), 400

    answer, status_code = register_user(data)
    if status_code != 201:
        return jsonify(answer), status_code

    serialized_user = user_response_schema.dump(answer['user'])
    return jsonify({
        "mensagem": answer['mensagem'],
        "token": answer['token'],
        "user": serialized_user
    }), 201

@user_bp.route('/register-page')
def register_page():
    return render_template('register.html')

@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_user_route():
    """Atualiza o perfil do usuário logado baseado no token JWT"""
    user_id = int(get_jwt_identity())

    try:
        partial_request_schema = UserRegistrationSchema(partial=True)
        data = partial_request_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    answer, status_code = update_user(user_id, data)
    if status_code != 200:
        return jsonify(answer), status_code

    serialized_user = user_response_schema.dump(answer['user'])
    return jsonify({
        "mensagem": answer['mensagem'],
        "user": serialized_user
    }), 200

@user_bp.route("/profile", methods=["DELETE"])
@jwt_required()
def delete_user_route():
    """Exclui a conta do usuário logado baseado no token JWT"""
    user_id = int(get_jwt_identity())

    answer, status_code = delete_user(user_id)
    return jsonify(answer), status_code