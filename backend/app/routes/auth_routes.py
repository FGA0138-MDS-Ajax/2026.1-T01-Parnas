from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

# Criação do módulo de rotas de autenticação
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validação básica para garantir a presença dos dados necessários
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

    email = data.get('email')
    password = data.get('password')

    # Executa a lógica de autenticação do serviço
    resultado, status_code = AuthService.login(email, password)

    return jsonify(resultado), status_code