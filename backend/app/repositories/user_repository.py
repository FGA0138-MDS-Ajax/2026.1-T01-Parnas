from app.config import db
from app.models.user import User


class UserRepository:

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
    def create(name, email, cpf, password_hash, birth_date, initial_company=None):
        new_user = User(
            name=name,
            email=email,
            cpf=cpf,
            password_hash=password_hash,
            birth_date=birth_date
        )

        if initial_company:
            # Adiciona na tabela de associação N:N
            new_user.companies.append(initial_company)
            # Define como a empresa ativa padrão
            new_user.company_id = initial_company.company_id

        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_active_company(user_id, company_id):
        user = UserRepository.get_by_id(user_id)
        if user:
            user.company_id = company_id
            db.session.commit()
            return True
        return False

    @staticmethod
    def list_companies(user_id):
        user = UserRepository.get_by_id(user_id)
        return user.companies if user else []