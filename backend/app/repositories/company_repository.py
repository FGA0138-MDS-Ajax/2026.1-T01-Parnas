import re
from app.config import db
from app.models.company import  Company
from app.models.user_company_association import user_company

class CompanyRepository:

    @staticmethod
    def get_by_id(company_id):
        return Company.query.get(company_id)

    @staticmethod
    def get_by_cnpj(cnpj):
        cnpj_clean = re.sub(r'\D', '', cnpj)
        return Company.query.filter_by(cnpj=cnpj_clean).first()

    @staticmethod
    def create(name,cnpj,email,phone,register_date):
        
        new_company = Company(
            name=name,
            cnpj=cnpj,
            email=email,
            phone=phone,
            register_date=register_date

        )

        db.session.add(new_company)
        db.session.commit()
        return new_company

    @staticmethod
    def save(company):
        db.session.add(company)
        db.session.commit()
        return company

    @staticmethod
    def delete(company):
        db.session.delete(company)
        db.session.commit()

    @staticmethod
    def attach_user(company_id, user_id):
        """Vincula um usuário a uma empresa na tabela user_company."""
        stmt = user_company.insert().values(user_id=user_id, company_id=company_id)
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod
    def check_user_access(company_id, user_id):
        """Verifica se um usuário tem acesso a empresa."""
        return db.session.query(user_company).filter(
            user_company.c.user_id == user_id,
            user_company.c.company_id == company_id
        ).first() is not None

    @staticmethod
    def get_all_by_user(user_id):
        return Company.query.join(user_company).filter(user_company.c.user_id == user_id).all()
