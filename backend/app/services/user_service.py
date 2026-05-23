import bcrypt
from app.models.user import User
from app.config import db
from app.utils.validators import is_valid_password, is_valid_birth_date
import jwt
import datetime
import os

def register_user(data):
    name = data.get('name')
    email = data.get('email')
    cpf = data.get('cpf') 
    password = data.get('password')
    birth_date_str = data.get('birth_date')
    
    if find_user_by_email(email):
        return {"erro": "Este e-mail já está cadastrado"}, 409

    if find_user_by_cpf(cpf):
        return {"erro": "Este CPF já está cadastrado"}, 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = User(
        name=name,
        email=email,
        cpf=cpf,
        password_hash=hashed_password,
        birth_date=birth_date_str
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        playload = {
            'user_id': new_user.id,
            'expiration_date': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        }

        secret_key = os.getenv('JWT_SECRET_KEY', 'chave-fallback-parnas-local')
        token = jwt.encode(playload, secret_key, algorithm='HS256')

        return {"mensagem": "Conta criada com sucesso.",
                "token": token
                }, 201

    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao tentar salvar o usuário."}, 500
    
def find_user_by_cpf(cpf: str):
    if not cpf:
        return None
    return db.session.query(User).filter(User.cpf==cpf).first()

def find_user_by_email(email: str):
    if not email:
        return None
    return db.session.query(User).filter(User.email == email).first()