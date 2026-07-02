import bcrypt
from flask_jwt_extended import create_access_token
from datetime import datetime, date
from app.repositories.user_repository import UserRepository
from app.exceptions.api_exception import APIException

class UserService:
    @staticmethod
    def register_user(data):
        name = data.get('name')
        email = data.get('email')
        raw_cpf = data.get('cpf')
        cpf = ''.join(filter(str.isdigit, raw_cpf)) if raw_cpf else None
        password = data.get('password')
        birth_date_raw = data.get('birth_date')

        if not all([name, email, cpf, password, birth_date_raw]):
            raise APIException("Todos os campos são obrigatórios.", 400)
        
        if isinstance(birth_date_raw, str):
            birth_date = datetime.strptime(birth_date_raw, '%Y-%m-%d').date()
        else:
            birth_date = birth_date_raw

        if UserRepository.get_by_email(email):
            raise APIException("Este e-mail já está cadastrado.", 409)
        
        if UserRepository.get_by_cpf(cpf):
            raise APIException("Este CPF já está cadastrado.", 409)
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            new_user = UserRepository.create(
                name=name,
                email=email,
                cpf=cpf,
                password_hash=hashed_password,
                birth_date=birth_date
            )
            token = create_access_token(identity=str(new_user.user_id))
            return {
                "mensagem": "Conta criada com sucesso.",
                "token": token,
                "user": new_user
            }, 201
        except Exception as e:
            return {"erro": f"Ocorreu um erro interno ao tentar salvar o usuário: {str(e)}"}, 500


    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise APIException("Usuário não encontrado.", 404)
        
        try:
            # Soft delete: desativa a conta em vez de remover do banco
            user.is_active = False
            UserRepository.save(user)
            return {"mensagem": "Usuário excluído com sucesso."}, 200
        except Exception as e:
            return {"erro": f"Ocorreu um erro interno ao tentar deletar o usuário: {str(e)}"}, 500


    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise APIException("Usuário não encontrado.", 404)
        
        email = data.get('email')
        if email and email != user.email:
            if UserRepository.get_by_email(email):
                raise APIException("Este e-mail já está em uso por outra conta.", 409)
            user.email = email
            
        raw_cpf = data.get('cpf')
        if raw_cpf:
            cpf = ''.join(filter(str.isdigit, raw_cpf))
            if cpf != user.cpf:
                if UserRepository.get_by_cpf(cpf):
                    raise APIException("Este CPF já está em uso por outra conta.", 409)
                user.cpf = cpf

        if 'name' in data:
            user.name = data['name']

        if 'birth_date' in data:
            try:
                user.birth_date = datetime.strptime(data.get('birth_date'), '%Y-%m-%d').date()
            except ValueError:
                return {"erro": "Formato de data de nascimento inválido. Use AAAA-MM-DD."}, 400
            
        try:
            UserRepository.save(user)
            return {"mensagem": "Dados do usuário atualizados com sucesso.", "user": user}, 200
        except Exception as e:
            return {"erro": f"Ocorreu um erro interno ao tentar atualizar o usuário: {str(e)}"}, 500