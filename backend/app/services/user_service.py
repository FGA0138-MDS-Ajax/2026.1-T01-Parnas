import bcrypt
from flask_jwt_extended import create_access_token
from app.models.company import Company
from app.models.user import User
from app.config import db
from datetime import datetime,date

def register_user(data):
    name = data.get('name')
    email = data.get('email')
    raw_cpf = data.get('cpf')
    cpf = ''.join(filter(str.isdigit, raw_cpf)) if raw_cpf else None
    password = data.get('password')
    birth_date_raw = data.get('birth_date')
    if isinstance(birth_date_raw, str):
        birth_date = datetime.strptime(birth_date_raw, '%Y-%m-%d').date()
    else:
        birth_date = birth_date_raw
    
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
        register_date=date.today()
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        token = create_access_token(identity=str(new_user.user_id))

        return {
            "mensagem": "Conta criada com sucesso.",
            "token": token,
            "user": new_user
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"erro": f"Ocorreu um erro interno ao tentar salvar o usuário. message: {str(e)}"}, 500
    
def find_user_by_cpf(cpf: str):
    if not cpf:
        return None
    cleaned_cpf = ''.join(filter(str.isdigit, cpf))
    return db.session.query(User).filter(User.cpf == cleaned_cpf).first()

def find_user_by_email(email: str):
    if not email:
        return None
    return db.session.query(User).filter(User.email == email).first()

def delete_user(user_id):
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"erro": "Usuário não encontrado."}, 404
    try:
        # Aplica o soft delete em vez de deletar fisicamente do banco
        user.is_active = False
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

    raw_cpf = data.get('cpf')
    if raw_cpf:
        cpf = ''.join(filter(str.isdigit, raw_cpf))
        if cpf != user.cpf:
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
        return {"mensagem": "Dados do usuário atualizados com sucesso.", "user": user}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao tentar atualizar o usuário."}, 500

