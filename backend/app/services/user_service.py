import bcrypt
from flask_jwt_extended import create_access_token
from app.models.company import Company
from app.models.user import User
from app.config import db
from datetime import datetime

def register_user(data):
    name = data.get('name')
    email = data.get('email')
    cpf = data.get('cpf') 
    password = data.get('password')
    birth_date = datetime.strptime(data.get('birth_date'),'%Y-%m-%d').date()
    
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
        birth_date=birth_date,
        register_date=datetime.utcnow()
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        token = create_access_token(identity=str(new_user.user_id))

        return {"mensagem": "Conta criada com sucesso.",
                "token": token
                }, 201

    except Exception as e:
        db.session.rollback()
        return {"erro": f"Ocorreu um erro interno ao tentar salvar o usuário. message: {str(e)}"}, 500
    
def find_user_by_cpf(cpf: str):
    if not cpf:
        return None
    return db.session.query(User).filter(User.cpf==cpf).first()

def find_user_by_email(email: str):
    if not email:
        return None
    return db.session.query(User).filter(User.email == email).first()

def delete_user(user_id):
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"erro": "Usuário não encontrado."}, 404
    try:
        db.session.delete(user)
        db.session.commit()
        return {"mensagem": "Usuário excluído com sucesso."}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao tentar excluir o usuário."}, 500

def update_user(user_id, data):
    user = db.session.query(User).filter(User.user_id == user_id).first()

    if not user:
        return {"erro": "Usuário não encontrado."}, 404

    email = data.get('email')
    if email and email != user.email:
        if find_user_by_email(email):
            return {"erro": "Este e-mail já está em uso por outra conta."}, 409
        user.email = email

    cpf = data.get('cpf')
    if cpf and cpf != user.cpf:
        if find_user_by_cpf(cpf):
            return {"erro": "Este CPF já está em uso por outra conta."}, 409
        user.cpf = cpf

    if 'name' in data:
        user.name = data['name']

    if 'birth_date' in data:
        try:
            user.birth_date = datetime.strptime(data.get('birth_date'), '%Y-%m-%d').date()
        except ValueError:
            return {"erro": "Formato de data de nascimento inválido. Use AAAA-MM-DD."}, 400

    try:
        db.session.commit()
        return {"mensagem": "Dados do usuário atualizados com sucesso."}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao tentar atualizar o usuário."}, 500

