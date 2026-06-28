from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from app.exceptions.api_exception import APIException
from app.schemas.company_schema import (
    CompanyRegistrationSchema,
    CompanyRequirements,
)
from app.services.company_service import (
    delete_company,
    get_all_companies,
    get_company,
    register_company,
    update_company,
)

company_bp = Blueprint("company_bp", __name__)
company_schema = CompanyRegistrationSchema()
company_output_schema = CompanyRequirements()

@company_bp.route("", methods=["POST"], strict_slashes=False)
@jwt_required()
def register_company_route():
    user_id = int(get_jwt_identity())
    try:
        data = company_schema.load(request.get_json())
    except ValidationError as error:
        return jsonify({"erros_de_validacao": error.messages}), 400
    try:
        answer, status_code = register_company(user_id=user_id, data=data)
    except APIException as e:
        return jsonify({"erro": e.message}), e.status_code
    if status_code == 201 and "company" in answer:
        answer["company"] = company_output_schema.dump(answer["company"])
    return jsonify(answer), status_code


@company_bp.route("/<int:company_id>", methods=["DELETE"])
@jwt_required()
def delete_company_route(company_id):
    user_id = int(get_jwt_identity())
    try:
        answer, status_code = delete_company(
            company_id=company_id,
            user_id=user_id,
        )
    except APIException as e:
        return jsonify({"erro": e.message}), e.status_code
    return jsonify(answer), status_code


@company_bp.route("/<int:company_id>", methods=["PUT"])
@jwt_required()
def update_company_route(company_id):
    user_id = int(get_jwt_identity())
    try:
        data = company_schema.load(request.get_json(), partial=True)
    except ValidationError as error:
        return jsonify({"erros_de_validacao": error.messages}), 400
    try:
        answer, status_code = update_company(
            data=data,
            user_id=user_id,
            company_id=company_id,
        )
    except APIException as e:
        return jsonify({"erro": e.message}), e.status_code
    if status_code == 200 and "company" in answer:
        answer["company"] = company_output_schema.dump(answer["company"])
    return jsonify(answer), status_code


@company_bp.route("/<int:company_id>", methods=["GET"])
@jwt_required()
def get_company_route(company_id):
    user_id = int(get_jwt_identity())
    try:
        answer, status_code = get_company(
            user_id=user_id,
            company_id=company_id,
        )
    except APIException as e:
        return jsonify({"erro": e.message}), e.status_code
    if "company" in answer:
        answer["company"] = company_output_schema.dump(answer["company"])
    return jsonify(answer), status_code


@company_bp.route("", methods=["GET"])
@jwt_required()
def get_all_companies_route():
    user_id = int(get_jwt_identity())
    answer, status_code = get_all_companies(user_id=user_id)
    if "companies" in answer:
        answer["companies"] = company_output_schema.dump(
            answer["companies"],
            many=True,
        )
    return jsonify(answer), status_code