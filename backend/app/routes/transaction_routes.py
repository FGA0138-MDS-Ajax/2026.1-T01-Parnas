from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.transaction_service import TransactionService

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    # Identifica quem é o usuário logado através do token
    current_user_id = get_jwt_identity()

    # Pega a paginação (com valores padrão de segurança)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Coleta todos os filtros enviados na URL
    filtros = {
        'data_inicio': request.args.get('data_inicio'),
        'data_fim': request.args.get('data_fim'),
        'tipo': request.args.get('tipo'),
        'categoria': request.args.get('categoria'),
        'valor_min': request.args.get('valor_min', type=float),
        'valor_max': request.args.get('valor_max', type=float)
    }

    resultado, status_code = TransactionService.get_history(current_user_id, page, per_page, filtros)

    return jsonify(resultado), status_code