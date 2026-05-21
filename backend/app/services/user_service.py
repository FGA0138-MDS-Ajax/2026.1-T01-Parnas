from datetime import datetime
from app.models.user import User
from app.config import db
from app.utils.validators import is_valid_password, is_valid_birth_date


def register_user(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    birth_date_str = data.get('birth_date')

    if not is_valid_password(password):
        return {"erro": "A senha não atende aos requisitos mínimos de segurança."}, 400

    if not is_valid_birth_date(birth_date_str):
        return {"erro": "A data de nascimento é inválida ou o usuário é menor de 18 anos"}, 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"erro": "Este e-mail já está cadastrado"}, 409
    return {"mensagem": "Deu bom"}, 200