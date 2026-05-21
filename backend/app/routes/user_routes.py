from flask import Blueprint, request, jsonify
from app.services.user_service import register_user
from app.schemas.user_schema import UserRegistrationSchema
from marshmallow import ValidationError

user_bp = Blueprint("user_bp", __name__)

user_schema = UserRegistrationSchema()

@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = user_schema.load(request.get_json())

    except ValidationError as err:
        return jsonify({"erros_de_validcao": err.messages}), 400

    answer, status_code = register_user(data)
    return jsonify(answer), status_code