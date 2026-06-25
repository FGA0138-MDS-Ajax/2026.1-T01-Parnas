import bcrypt
from flask_jwt_extended import create_access_token
from app.services.user_service import find_user_by_email


class AuthService:
    @staticmethod
    def login(email, password):
        # 1. Busca o usuário usando a função do banco de dados
        user = find_user_by_email(email)

        # Se o usuário não existir OU estiver desativado (soft delete), retorna o erro 401 solicitado
        if not user or not user.is_active:
            return {"erro": "Conta não encontrada ou desativada"}, 401

        # 2. Valida se a senha bate com o hash do banco usando bcrypt (.encode converte para bytes)
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return {"erro": "E-mail ou senha inválidos"}, 401

        # 3. Gera o token JWT usando o ID do usuário cadastrado
        token = create_access_token(identity=str(user.user_id))

        return {"token": token}, 200