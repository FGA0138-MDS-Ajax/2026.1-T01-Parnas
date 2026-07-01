from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.transaction_schema import TransactionSchema, TransactionRequirements
from marshmallow import ValidationError
from app.services.transaction_service import TransactionService

transaction_bp = Blueprint("transaction_bp", __name__)
transaction_schema = TransactionSchema()
transaction_output_schema = TransactionRequirements()

@transaction_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions(company_id):
    """
    Endpoint unificado: Retorna o histórico de transações paginado e filtrado,
    mas escopado obrigatoriamente por empresa para manter a segurança.
    """
    current_user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # adicionado user_id e company_id aos filtros para o repositório conseguir encontrar os dados
    filtros = {
        'user_id': current_user_id,
        'company_id': company_id,
        'data_inicio': request.args.get('data_inicio'),
        'data_fim': request.args.get('data_fim'),
        'tipo': request.args.get('tipo'),
        'categoria': request.args.get('categoria'),
        'valor_min': request.args.get('valor_min', type=float),
        'valor_max': request.args.get('valor_max', type=float)
    }
    resultado, status_code = TransactionService.get_history_filtered(current_user_id, company_id, page, per_page, filtros)
    return jsonify(resultado), status_code

@transaction_bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction_route(company_id):
    user_id = int(get_jwt_identity())
    json_data = request.get_json()
    
    # Captura o id da conta/caixa antes do validador descartar
    payment_id = json_data.get('payment_id')

    try:
        # CORREÇÃO: 'exclude' em minúsculo para ignorar campos fora do Schema
        data = transaction_schema.load(json_data, unknown='exclude')
    except ValidationError as err:
        return jsonify({"erros": err.messages}), 400

    # Injeta o payment_id de volta no dicionário de dados limpos
    if payment_id is not None:
        data['payment_id'] = payment_id

    answer, status_code = TransactionService.create_transaction(user_id, company_id, data)
    return jsonify(answer), status_code


@transaction_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction_route(company_id, transaction_id):
    user_id = int(get_jwt_identity())
    json_data = request.get_json()
    payment_id = json_data.get('payment_id')

    try:
        data = transaction_schema.load(json_data, partial=True, unknown='exclude')
    except ValidationError as err:
        return jsonify({"erros": err.messages}), 400

    if payment_id is not None:
        data['payment_id'] = payment_id

    answer, status_code = TransactionService.update_transaction(user_id, company_id, transaction_id, data)
    return jsonify(answer), status_code

@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete(company_id, transaction_id): # adicionado o company_id para evitar o TypeError (Erro 500)

    # daniel: o service espera (transaction_id, user_id); estava passando o company_id
    # no lugar do user_id, escopando a exclusao pelo id errado.
    # o identity do JWT vem como string, entao converto pra int (igual as demais rotas).
    current_user_id = int(get_jwt_identity())
    answer, status_code = TransactionService.delete_transaction(current_user_id, transaction_id)
    return jsonify(answer), status_code