from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.bill_service import BillService

# Criação do módulo de rotas de contas
bill_bp = Blueprint('bills', __name__)


@bill_bp.route('/', methods=['POST'])
@jwt_required()
def create_bill():
    data = request.get_json()

    # Validação básica de campos obrigatórios
    required_fields = ['description', 'amount', 'type', 'due_date', 'category_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"erro": "Faltam campos obrigatórios."}), 400

    resultado, status_code = BillService.create_bill(data)
    return jsonify(resultado), status_code


@bill_bp.route('/', methods=['GET'])
@jwt_required()
def get_bills():
    # Permite filtrar por status passando ?status=pendente na URL
    status = request.args.get('status', 'Pendente')

    if status.lower() == 'todas':
        status = None

    resultado, status_code = BillService.get_bills(status)
    return jsonify(resultado), status_code


@bill_bp.route('/<int:bill_id>', methods=['PUT'])
@jwt_required()
def update_bill(bill_id):
    data = request.get_json()

    resultado, status_code = BillService.update_bill(bill_id, data)
    return jsonify(resultado), status_code


@bill_bp.route('/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(bill_id):

    resultado, status_code = BillService.delete_bill(bill_id)
    return jsonify(resultado), status_code


@bill_bp.route('/<int:bill_id>/quitar', methods=['PATCH'])
@jwt_required()
def pay_bill(bill_id):

    current_user_id = int(get_jwt_identity())

    resultado, status_code = BillService.pay_bill(current_user_id, bill_id)
    return jsonify(resultado), status_code