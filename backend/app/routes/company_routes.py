from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.company_service import register_company, delete_company, update_company
from app.schemas.company_schema import CompanyRegistrationSchema, CompanyDeleteSchema, CompanyRequirements
from marshmallow import ValidationError

company_bp = Blueprint("company_bp", __name__)

company_schema = CompanyRegistrationSchema()
company_delete_schema = CompanyDeleteSchema()
company_output_schema = CompanyRequirements()

@company_bp.route("/register", methods=["POST"])
@jwt_required()
def register_company_route():    
    
    user_id = int(get_jwt_identity())
    
    try:
        data = company_schema.load(request.get_json())

    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400
    
    answer, status_code = register_company(user_id, data)

    if status_code == 201 and "company" in answer:
        answer["company"] = company_output_schema.dump(answer["company"])
        
    return jsonify(answer), status_code

@company_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_company_route():
    
    user_id = int(get_jwt_identity())
    try:
        data = company_delete_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    answer, status_code = delete_company()
    return jsonify(answer), status_code


@company_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_company_route():
    user_id = int(get_jwt_identity())
    raw_data = request.get_json()

    try:
        validated_data = company_schema.load(raw_data, partial=True)
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    answer, status_code = update_company(validated_data)
    
    if status_code == 200 and "company" in answer:
        answer["company"] = company_output_schema.dump(answer["company"])
        
    return jsonify(answer), status_code