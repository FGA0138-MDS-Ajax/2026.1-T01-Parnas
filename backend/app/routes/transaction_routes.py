from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.transaction_schema import TransactionSchema
from marshmallow import ValidationError
from app.services.transaction_service import (
    create_transaction,
    get_company_transactions,
    update_transaction,
    delete_transaction
)

transaction_bp = Blueprint("transaction_bp", __name__)
transaction_schema = TransactionSchema()

@transaction_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    try:
        date = transaction_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    current_user_id = get_jwt_identity()
    answer, status_code = create_transaction(date, current_user_id)
    return jsonify(answer), status_code

@transaction_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update(transaction_id):
    date = request.get_json()
    company_id = date.get("company_id")

    if not company_id:
        return jsonify({"erro": "O company_id é obrigatório no corpo da requisição."}), 400

    answer, status_code = update_transaction(transaction_id, date, company_id)
    return jsonify(answer), status_code

@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete(transaction_id):
    company_id = request.args.get('company_id')

    if not company_id:
        return jsonify({"erro": "O parâmetro company_id é obrigatório."}), 400

    answer, status_code = delete_transaction(transaction_id, company_id)
    return jsonify(answer), status_code