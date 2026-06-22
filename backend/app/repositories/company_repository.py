from app.models.user_company_association import user_company
from app.models.company import Company
from app.config import db
from app.exceptions.api_exception import APIException
import re

class CompanyRepository:
    @staticmethod
    def get_by_id(company_id):
        return Company.query.filter_by(company_id=company_id).first()
    
    @staticmethod
    def get_by_cnpj(cnpj):
        cnpj_clean = re.sub(r'\D', '', cnpj)
        company = Company.query.filter_by(cnpj=cnpj_clean).first()
        return company
    
    @staticmethod
    def check_access(company_id, user_id):
        if not (db.session.query(user_company).filter_by(user_id=user_id, company_id=company_id).first()):
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
        
    @staticmethod
    def get_all_by_user(user_id):
        return Company.query.join(user_company).filter(user_company.c.user_id == user_id).all()
    
    @staticmethod
    def create(name, cnpj, email, phone, user_id):
        cnpj_clean = re.sub(r'\D', '', cnpj)

        if(CompanyRepository.get_by_cnpj(cnpj_clean)):
            raise APIException("CNPJ já cadastrado.", 409)
        
        new_company = Company(
            name=name,
            cnpj=cnpj_clean,
            email=email,
            phone=phone
        )
        db.session.add(new_company)
        db.session.flush()

        UserCompany = user_company.insert().values(
            user_id=user_id,
            company_id=new_company.company_id,
        )
        db.session.execute(UserCompany)
        db.session.commit()

        return new_company

    @staticmethod
    def delete(company_id):
        company = CompanyRepository.get_by_id(company_id)
        
        db.session.delete(company)
        db.session.commit()
    
