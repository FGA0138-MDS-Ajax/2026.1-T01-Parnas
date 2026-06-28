from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.transaction_schema import TransactionSchema, TransactionRequirements
from marshmallow import ValidationError
from app.services.transaction_service import (
    get_history_filtered, # Para o método get_history do histórico
    create_transaction,
    update_transaction,
    delete_transaction
)

transaction_bp = Blueprint("transaction_bp", __name__)
transaction_schema = TransactionSchema()
transaction_output_schema = TransactionRequirements()

@transaction_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    """
    Endpoint unificado: Retorna o histórico de transações paginado e filtrado,
    mas escopado obrigatoriamente por empresa para manter a segurança.
    """
    current_user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    filtros = {
        'data_inicio': request.args.get('data_inicio'),
        'data_fim': request.args.get('data_fim'),
        'tipo': request.args.get('tipo'),
        'categoria': request.args.get('categoria'),
        'valor_min': request.args.get('valor_min', type=float),
        'valor_max': request.args.get('valor_max', type=float)
    }
    resultado, status_code = get_history_filtered(current_user_id, page, per_page, filtros)
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
    
    if status_code == 201 and "transaction" in answer:
        answer["transaction"] = transaction_output_schema.dump(answer["transaction"])
        
    return jsonify(answer), status_code
@transaction_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update(transaction_id):
    raw_data = request.get_json()

    try:
        validated_data = transaction_schema.load(raw_data, partial=True)
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    # daniel: o service espera (transaction_id, user_id, data); estava passando o dict
    # de dados como user_id e o company_id como data, o que quebrava a edicao.
    # o identity do JWT vem como string, entao converto pra int (igual as demais rotas).
    current_user_id = int(get_jwt_identity())
    answer, status_code = update_transaction(transaction_id, current_user_id, validated_data)
    
    if status_code == 200 and "transaction" in answer:
        answer["transaction"] = transaction_output_schema.dump(answer["transaction"])
        
    return jsonify(answer), status_code

@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete(transaction_id):

    # daniel: o service espera (transaction_id, user_id); estava passando o company_id
    # no lugar do user_id, escopando a exclusao pelo id errado.
    # o identity do JWT vem como string, entao converto pra int (igual as demais rotas).
    current_user_id = int(get_jwt_identity())
    answer, status_code = delete_transaction(transaction_id, current_user_id)
    return jsonify(answer), status_code