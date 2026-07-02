import bcrypt
from flask_jwt_extended import create_access_token
from app.repositories.user_repository import UserRepository


def login(email, password):
    # 1. Busca o usuário usando o UserRepository atualizado
    user = UserRepository.get_by_email(email)

    # Se o usuário não existir, retorna o erro 401 de segurança
    #anna: corrigindo as mensagens para indicar exatamente qual o erro com o login
    if not user:
        return {"erro": "E-mail não encontrado. Verifique o endereço de e-mail digitado."}, 401

    # Se o usuário estiver desativado (soft delete), bloqueia o login
    if not user.is_active:
        return {"erro": "Conta não encontrada ou desativada"}, 401

    # 2. Valida se a senha bate com o hash do banco usando bcrypt (.encode converte para bytes)
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return {"erro": "E-mail ou senha inválidos"}, 401

    # 3. Gera o token JWT usando o ID do usuário cadastrado
    token = create_access_token(identity=str(user.user_id))
    return {"token": token}, 200