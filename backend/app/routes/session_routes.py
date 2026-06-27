from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.session_service import SessionService

session_bp = Blueprint('session', __name__)


@session_bp.route('/usuarios/me/empresas', methods=['GET'])
@jwt_required()
def get_my_companies():
    """Lista as empresas do usuário logado"""
    current_user_id = get_jwt_identity()
    resultado, status_code = SessionService.get_user_companies(current_user_id)
    return jsonify(resultado), status_code


@session_bp.route('/sessao/empresa-ativa', methods=['POST'])
@jwt_required()
def set_active_company():
    """Define a empresa ativa e retorna um novo JWT token"""
    current_user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    company_id = data.get('company_id')

    if not company_id:
        return jsonify({"erro": "O company_id é obrigatório"}), 400

    resultado, status_code = SessionService.set_active_company(current_user_id, company_id)
    return jsonify(resultado), status_code
