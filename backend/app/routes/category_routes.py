from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.category_service import add_category, get_categories, update_category, delete_category
from app.schemas.category_schema import CategoryAddSchema, CategoryRequirements
from marshmallow import ValidationError

category_bp = Blueprint("category_bp", __name__)
category_schema = CategoryAddSchema()
category_output_schema = CategoryRequirements()


@category_bp.route("/", methods=["POST"])
@jwt_required()
def add_category_route(company_id):
    user_id = int(get_jwt_identity())
    try:
        data = category_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    answer, status_code = add_category(user_id=user_id, company_id=company_id, data=data)

    if status_code == 201 and "category" in answer:
        answer["category"] = category_output_schema.dump(answer["category"])

    return jsonify(answer), status_code


@category_bp.route("/", methods=["GET"])
@jwt_required()
def get_categories_route(company_id):
    user_id = int(get_jwt_identity())

    answer, status_code = get_categories(user_id=user_id, company_id=company_id)

    if status_code == 200 and "categories" in answer:
        answer["categories"] = category_output_schema.dump(answer["categories"], many=True)

    return jsonify(answer), status_code


@category_bp.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category_route(company_id, category_id):
    user_id = int(get_jwt_identity())

    try:
        data = category_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    answer, status_code = update_category(
        user_id=user_id,
        company_id=company_id,
        category_id=category_id,
        data=data
    )

    if status_code == 200 and "category" in answer:
        answer["category"] = category_output_schema.dump(answer["category"])

    return jsonify(answer), status_code


@category_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category_route(company_id, category_id):
    user_id = int(get_jwt_identity())

    answer, status_code = delete_category(
        user_id=user_id,
        company_id=company_id,
        category_id=category_id,
    )

    return jsonify(answer), status_code