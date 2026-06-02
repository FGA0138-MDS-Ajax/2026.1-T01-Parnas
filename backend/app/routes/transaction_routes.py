from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.transaction_schema import TransactionSchema
from marshmallow import ValidationError
from app.services.transaction_service import (
    TransactionService, # Para o método get_history do histórico
    create_transaction,
    update_transaction,
    delete_transaction
)

transaction_bp = Blueprint("transaction_bp", __name__)
transaction_schema = TransactionSchema()

@transaction_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    """
    Endpoint unificado: Retorna o histórico de transações paginado e filtrado,
    mas escopado obrigatoriamente por empresa para manter a segurança.
    """
    current_user_id = get_jwt_identity()
    company_id = request.args.get('company_id', type=int)

    if not company_id:
        return jsonify({"erro": "O parâmetro company_id é obrigatório."}), 400

    # Coleta a paginação enviada na URL (com valores padrão seguros)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Coleta todos os filtros dinâmicos enviados na URL
    filtros = {
        'company_id': company_id, # Injetamos a empresa obrigatoriamente nos filtros
        'data_inicio': request.args.get('data_inicio'),
        'data_fim': request.args.get('data_fim'),
        'tipo': request.args.get('tipo'),
        'categoria': request.args.get('categoria'),
        'valor_min': request.args.get('valor_min', type=float),
        'valor_max': request.args.get('valor_max', type=float)
    }

    # Chama a service de histórico que veio da branch 7
    resultado, status_code = TransactionService.get_history(current_user_id, page, per_page, filtros)

    return jsonify(resultado), status_code

@transaction_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    try:
        data = transaction_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    current_user_id = get_jwt_identity()
    answer, status_code = create_transaction(data, current_user_id)
    return jsonify(answer), status_code

@transaction_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update(transaction_id):
    data = request.get_json()
    company_id = data.get("company_id")

    if not company_id:
        return jsonify({"erro": "O company_id é obrigatório no corpo da requisição."}), 400

    answer, status_code = update_transaction(transaction_id, data, company_id)
    return jsonify(answer), status_code

@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete(transaction_id):
    company_id = request.args.get('company_id')

    if not company_id:
        return jsonify({"erro": "O parâmetro company_id é obrigatório."}), 400

    answer, status_code = delete_transaction(transaction_id, company_id)
    return jsonify(answer), status_code
