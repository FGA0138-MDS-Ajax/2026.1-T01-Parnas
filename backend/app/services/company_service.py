from app.models.company import Company
from app.models.user_company import UserCompany
from app.config import db
import re

def register_company(user_id, data):
     try:
          name = data.get('name')
          cnpj = data.get('cnpj')
          email = data.get('email')
          phone = data.get('phone')

          cnpj_clean = re.sub(r'\D', '', cnpj)
          
          existing_company = Company.query.filter_by(cnpj=cnpj_clean).first()
          if existing_company:
               return {"erro": "CNPJ já cadastrado"}, 409
          
          new_company = Company(
               name=name,
               cnpj=cnpj_clean,
               email=email,
               phone=phone
          )
          db.session.add(new_company)
          db.session.flush()

          user_company = UserCompany(
               user_id=user_id,
               company_id=new_company.company_id,
               role='admin'
          )
          db.session.add(user_company)
          db.session.commit()

          return {"mensagem": "Empresa cadastrada com sucesso",
               "company_id": new_company.company_id,
               "name": new_company.name,
               "cnpj": new_company.cnpj}, 201
     
     except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar empresa: {str(e)}")
        return {"erro": f"Ocorreu um erro interno ao tentar cadastrar a empresa: {str(e)}"}, 500