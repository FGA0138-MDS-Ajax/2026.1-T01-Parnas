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
def create_bill(company_id):
    user_id = int(get_jwt_identity())

    try:
        data = bill_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros": err.messages}), 400

    resultado, status_code = BillService.create_bill(user_id, company_id, data)
    return jsonify(resultado), status_code

@bill_bp.route('/', methods=['GET'])
@jwt_required()
def get_bills(company_id):
    user_id = int(get_jwt_identity())
    
    #pega o status enviado pelo frontend (se não enviar, será None)
    status = request.args.get('status')
    
    #normaliza para minúsculas para não dar conflito com o SQLite 
    if status:
        status = status.lower()
        if status == 'todas':
            status = None

    resultado, status_code = BillService.get_bills(user_id, company_id, status)
    return jsonify(resultado), status_code


@bill_bp.route('/<int:bill_id>', methods=['PUT'])
@jwt_required()
def update_bill(company_id, bill_id):
    user_id = int(get_jwt_identity())

    try:
        data = bill_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"erros": err.messages}), 400

    resultado, status_code = BillService.update_bill(user_id, company_id, bill_id, data)
    return jsonify(resultado), status_code


@bill_bp.route('/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(company_id, bill_id):
    user_id = int(get_jwt_identity())

    resultado, status_code = BillService.delete_bill(user_id, company_id, bill_id)
    return jsonify(resultado), status_code


@bill_bp.route('/<int:bill_id>/quitar', methods=['PATCH'])
@jwt_required()
def pay_bill(company_id, bill_id):
    user_id = int(get_jwt_identity())

    resultado, status_code = BillService.pay_bill(user_id, company_id, bill_id)
    return jsonify(resultado), status_code