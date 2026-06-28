from flask import Blueprint, request, jsonify, render_template
from app.services import auth_service  # Alterado: importando o módulo funcional
from app.repositories.user_repository import UserRepository  # Alterado: usa o repository para buscar e-mails
from app.utils.reset_token import generate_reset_token, verify_reset_token
import bcrypt
from app.config import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

    email = data.get('email')
    password = data.get('password')

    resultado, status_code = auth_service.login(email, password)

    return jsonify(resultado), status_code


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"erro": "Email obrigatório"}), 400

    user = UserRepository.get_by_email(email)

    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    token = generate_reset_token(user.email)
    reset_link = f"http://localhost:5173/esqueci-senha?token={token}"

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

    user = UserRepository.get_by_email(email)

    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    hashed_password = bcrypt.hashpw(
        new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    user.password_hash = hashed_password

    UserRepository.save(user)

    return jsonify({
        "mensagem": "Senha redefinida com sucesso"
    }), 200


@auth_bp.route('/forgot-password-page')
def forgot_password_page():
    return render_template('forgot_password.html')

@auth_bp.route('/reset-password/<token>')
def reset_password_page(token):
    return render_template('reset_password.html', token=token)