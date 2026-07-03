from flask import Blueprint, request, jsonify, render_template, current_app
from app.services import auth_service  # Alterado: importando o módulo funcional
from app.repositories.user_repository import UserRepository  # Alterado: usa o repository para buscar e-mails
from app.utils.reset_token import generate_reset_token, verify_reset_token
import bcrypt
from app.config import db
from flask_mail import Message  

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

    # Gera o token de reset baseado no email do usuário
    token = generate_reset_token(user.email)
    
    # Busca a URL do frontend (Vite) configurada no .env. Se não achar, usa o fallback na porta 5173
    frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5173').rstrip('/')
    reset_link = f"{frontend_url}/esqueci-senha?token={token}" 

    try:
        # Recupera a extensão 'mail' registrada no contexto atual da aplicação
        mail_extension = current_app.extensions.get('mail')

        msg = Message(
            subject="Recuperação de Senha - Credifab",
            recipients=[user.email]
        )
        
        # Texto alinhado à esquerda para evitar espaços em branco indesejados no e-mail recebido
        msg.body = f"""Olá!

Você solicitou a recuperação de senha para a sua conta no Credifab.
Para redefinir sua senha, clique no link abaixo ou copie e cole no seu navegador:

{reset_link}

Se você não solicitou essa alteração, ignore este e-mail."""

        # CORREÇÃO: Usa a variável mail_extension recuperada acima para enviar o e-mail
        mail_extension.send(msg)
        print(f"LOG: E-mail de recuperação enviado com sucesso para {user.email}")

    except Exception as e:
        print(f"LOG ERRO ENVIO EMAIL: {str(e)}")
        return jsonify({"erro": "Erro interno ao tentar enviar o e-mail de recuperação."}), 500

    return jsonify({
        "mensagem": "E-mail de recuperação enviado com sucesso",
        "email": user.email,
        "reset_link": reset_link  # <-- Adicione essa linha de volta!
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