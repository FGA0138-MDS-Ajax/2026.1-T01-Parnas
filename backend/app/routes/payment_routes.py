from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.schemas.payment_schema import PaymentAddSchema, PaymentRequirements
from app.services.payment_service import PaymentService

payment_bp = Blueprint("payment_bp", __name__)
payment_schema = PaymentAddSchema()
payment_output_schema = PaymentRequirements()


@payment_bp.route("/", methods=["POST"])
@jwt_required()
def add_category_route(company_id):
    user_id = int(get_jwt_identity())
    try:
        data = payment_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    answer, status_code = PaymentService.add_payment(user_id=user_id, company_id=company_id, data=data)

    if status_code == 201 and "payment" in answer:
        answer["payment"] = payment_output_schema.dump(answer["payment"])

    return jsonify(answer), status_code


@payment_bp.route("/", methods=["GET"])
@jwt_required()
def get_payments_route(company_id):
    user_id = int(get_jwt_identity())

    answer, status_code = PaymentService.get_payments(user_id=user_id, company_id=company_id)

    if status_code == 200 and "payments" in answer:
        answer["payments"] = payment_output_schema.dump(answer["payments"], many=True)

    return jsonify(answer), status_code


@payment_bp.route("/<int:payment_id>", methods=["PUT"])
@jwt_required()
def update_payment_route(company_id, payment_id):
    user_id = int(get_jwt_identity())

    try:
        data = payment_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    answer, status_code = PaymentService.update_payment(
        user_id=user_id,
        company_id=company_id,
        payment_id=payment_id,
        data=data
    )

    if status_code == 200 and "payment" in answer:
        answer["payment"] = payment_output_schema.dump(answer["payment"])

    return jsonify(answer), status_code


@payment_bp.route("/<int:payment_id>", methods=["DELETE"])
@jwt_required()
def delete_payment_route(company_id, payment_id):
    user_id = int(get_jwt_identity())

    answer, status_code = PaymentService.delete_payment(
        user_id=user_id,
        company_id=company_id,
        payment_id=payment_id,
    )

    return jsonify(answer), status_code