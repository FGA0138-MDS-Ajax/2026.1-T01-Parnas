from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    
    _base = BaseRepository(User)
    
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_cpf(cpf):
        return User.query.filter_by(cpf=cpf).first()
    
    @staticmethod
    def save(user):
        return UserRepository._base.save(user)
    
    @staticmethod
    def delete(user):
        UserRepository._base.delete(user)
    
    @staticmethod
    def create(name, email, cpf, password_hash, birth_date, initial_company=None):
        new_user = User(
            name=name,
            email=email,
            cpf=cpf,
            password_hash=password_hash,
            birth_date=birth_date
        )
        if initial_company:
            new_user.companies.append(initial_company)
            new_user.active_company_id = initial_company.company_id
        return UserRepository._base.save(new_user)
    
    @staticmethod
    def update_active_company(user_id, company_id):
        user = UserRepository.get_by_id(user_id)
        if user:
            user.active_company_id = company_id
            UserRepository._base.save(user)
            return True
        return False
    
    @staticmethod
    def list_companies(user_id):
        user = UserRepository.get_by_id(user_id)
        return user.companies if user else []