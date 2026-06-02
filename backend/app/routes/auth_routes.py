from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.services.user_service import find_user_by_email
from app.utils.reset_token import generate_reset_token
from app.utils.reset_token import verify_reset_token
import bcrypt
from app.config import db
from flask import Blueprint, request, jsonify, render_template

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

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()

    email = data.get('email')

    if not email:
        return jsonify({"erro": "Email obrigatório"}), 400

    user = find_user_by_email(email)

    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    token = generate_reset_token(user.email)

    reset_link = f"http://localhost:5000/auth/reset-password/{token}"

    return jsonify({
        "mensagem": "Token gerado",
        "reset_link": reset_link,
        "email": user.email
    }), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()

    token = data.get('token')
    new_password = data.get('new_password')

    if not token or not new_password:
        return jsonify({"erro": "Token e nova senha obrigatórios"}), 400

    email = verify_reset_token(token)

    if not email:
        return jsonify({"erro": "Token inválido ou expirado"}), 400

    user = find_user_by_email(email)

    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    hashed_password = bcrypt.hashpw(
        new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    user.password_hash = hashed_password

    db.session.commit()

    return jsonify({
        "mensagem": "Senha redefinida com sucesso"
    }), 200

@auth_bp.route('/forgot-password-page')
def forgot_password_page():
    return render_template('forgot_password.html')


@auth_bp.route('/reset-password/<token>')
def reset_password_page(token):
    return render_template('reset_password.html' ,token=token)