from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.services.bill_service import BillService
from app.schemas.bill_schema import BillSchema

# Criação do módulo de rotas de contas
bill_bp = Blueprint('bills', __name__)


bill_schema = BillSchema()
bills_schema = BillSchema(many=True)

@bill_bp.route('/', methods=['POST'])
@jwt_required()
def create_bill():
    try:
        data = bill_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros": err.messages}), 400

    resultado, status_code = BillService.create_bill(data)
    return jsonify(resultado), status_code

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
    try:
        data = bill_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"erros": err.messages}), 400

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