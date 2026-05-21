from flask import Blueprint, request, jsonify
from app.services.user_service import register_user

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    """
        Rota para cadastro de um novo usuário.

        Endpoint: POST /users/register

        Corpo da Requisição (JSON esperado):
        {
            "name": "Nome do Usuário",
            "email": "usuario@email.com",
            "cpf": "12345678900",
            "password": "SenhaForte123!",
            "birth_date": "2000-05-25" Formato YYYY-MM-DD
        }

        Possíveis respostas:
        - 201 (Created): Conta criada com sucesso.
        - 400 (Bad Request): Erro de validação (senha fraca ou menor de 16 anos).
        - 409 (Conflict): E-mail ou CPF já cadastrados no banco.
        - 500 (Server Error): Erro interno ao salvar no banco.
        """
    data = request.get_json()

    answer, status_code = register_user(data)
    return jsonify(answer), status_code