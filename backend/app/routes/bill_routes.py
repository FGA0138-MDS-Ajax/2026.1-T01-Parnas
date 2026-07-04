from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.services.bill_service import BillService
from app.schemas.bill_schema import BillSchema

bill_bp = Blueprint('bills', __name__)

bill_schema = BillSchema()
bills_schema = BillSchema(many=True)

@bill_bp.route('/', methods=['POST'])
@jwt_required()
def create_bill(company_id):
    user_id = int(get_jwt_identity())
    json_data = request.get_json()
    
    #anna: preserva o ID do caixa antes da validação
    payment_id = json_data.get('payment_id')

    try:
        #anna correção: Mudado de 'EXCLUDE' para 'exclude' (minúsculo)
        data = bill_schema.load(json_data, unknown='exclude')
    except ValidationError as err:
        mensagens_erro = []
        for campo, erros in err.messages.items():
            mensagens_erro.append(f"'{campo}' ({', '.join(erros)})")
        
        texto_final = "Erro de validação no formulário: " + " | ".join(mensagens_erro)
        return jsonify({"erro": texto_final}), 400

    if payment_id is not None:
        data['payment_id'] = payment_id

    resultado, status_code = BillService.create_bill(user_id, company_id, data)
    return jsonify(resultado), status_code


@bill_bp.route('/', methods=['GET'])
@jwt_required()
def get_bills(company_id):
    user_id = int(get_jwt_identity())
    status = request.args.get('status')
    
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
    json_data = request.get_json()
    payment_id = json_data.get('payment_id')

    try:
        #anna correção: Mudado de 'EXCLUDE' para 'exclude' (minúsculo)
        data = bill_schema.load(json_data, partial=True, unknown='exclude')
    except ValidationError as err:
        mensagens_erro = []
        for campo, erros in err.messages.items():
            mensagens_erro.append(f"'{campo}' ({', '.join(erros)})")
        return jsonify({"erro": " | ".join(mensagens_erro)}), 400

    if payment_id is not None:
        data['payment_id'] = payment_id

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