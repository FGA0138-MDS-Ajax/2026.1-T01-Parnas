from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.category_service import add_category
from app.schemas.category_schema import CategoryAddSchema
from marshmallow import ValidationError

category_bp = Blueprint("category_bp", __name__)

category_schema = CategoryAddSchema()

@category_bp.route("", methods=["POST"])
@jwt_required()
def add_category_route():
    user_id = int(get_jwt_identity())
    try:
        data = category_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400
    
    answer, status_code = add_category(user_id, data)
    return jsonify(answer), status_code