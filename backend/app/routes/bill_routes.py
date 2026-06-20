from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import bill_service

bill_bp = Blueprint('bills', __name__)

@bill_bp.route('/', methods=['POST'])
@jwt_required()
def create_bill():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    required_fields = ['description', 'amount', 'type', 'due_date', 'category_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"erro": "Faltam campos obrigatórios."}), 400

    resultado, status_code = bill_service.create_bill(current_user_id, data)
    return jsonify(resultado), status_code


@bill_bp.route('/', methods=['GET'])
@jwt_required()
def get_bills():
    current_user_id = get_jwt_identity()
    status = request.args.get('status')

    resultado, status_code = bill_service.get_bills(current_user_id, status)
    return jsonify(resultado), status_code


@bill_bp.route('/<int:bill_id>', methods=['PUT'])
@jwt_required()
def update_bill(bill_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()

    resultado, status_code = bill_service.update_bill(current_user_id, bill_id, data)
    return jsonify(resultado), status_code

@bill_bp.route('/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(bill_id):
    current_user_id = get_jwt_identity()

    resultado, status_code = bill_service.delete_bill(current_user_id, bill_id)
    return jsonify(resultado), status_code

@bill_bp.route('/<int:bill_id>/quitar', methods=['PATCH'])
@jwt_required()
def pay_bill(bill_id):
    current_user_id = get_jwt_identity()

    resultado, status_code = bill_service.pay_bill(current_user_id, bill_id)
    return jsonify(resultado), status_code