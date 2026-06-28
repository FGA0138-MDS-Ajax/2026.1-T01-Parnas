from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import bill_service

bill_bp = Blueprint('bills', __name__)

@bill_bp.route('/', methods=['POST'])
@jwt_required()
def create_bill():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    required_fields = ['description', 'amount', 'type', 'due_date', 'category_id', 'company_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"erro": "Faltam campos obrigatórios (incluindo company_id)."}), 400

    resultado, status_code = BillService.create_bill(current_user_id, data)
    return jsonify(resultado), status_code

@bill_bp.route('/', methods=['GET'])
@jwt_required()
def get_bills():
    current_user_id = int(get_jwt_identity())
    company_id = request.args.get('company_id', type=int)
    status = request.args.get('status')

    if not company_id:
        return jsonify({"erro": "O parâmetro company_id é obrigatório na URL."}), 400

    resultado, status_code = BillService.get_bills(current_user_id, company_id, status)
    return jsonify(resultado), status_code

@bill_bp.route('/<int:bill_id>', methods=['PUT'])
@jwt_required()
def update_bill(bill_id):
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    company_id = data.get('company_id')
    if not company_id:
        return jsonify({"erro": "O company_id é obrigatório no corpo da requisição."}), 400

    resultado, status_code = BillService.update_bill(current_user_id, company_id, bill_id, data)
    return jsonify(resultado), status_code

@bill_bp.route('/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(bill_id):
    current_user_id = int(get_jwt_identity())
    company_id = request.args.get('company_id', type=int)

    if not company_id:
        return jsonify({"erro": "O parâmetro company_id é obrigatório na URL."}), 400

    resultado, status_code = BillService.delete_bill(current_user_id, company_id, bill_id)
    return jsonify(resultado), status_code

@bill_bp.route('/<int:bill_id>/quitar', methods=['PATCH'])
@jwt_required()
def pay_bill(bill_id):
    current_user_id = int(get_jwt_identity())
    company_id = request.args.get('company_id', type=int)

    if not company_id:
        return jsonify({"erro": "O parâmetro company_id é obrigatório na URL."}), 400

    resultado, status_code = BillService.pay_bill(current_user_id, company_id, bill_id)
    return jsonify(resultado), status_code