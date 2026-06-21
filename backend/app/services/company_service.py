from app.models.company import Company
from app.models.user_company_association import user_company
from app.config import db
import re
from app.repositories.company_repository import CompanyRepository
from app.exceptions.api_exception import APIException

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

          UserCompany = user_company.insert().values(
               user_id=user_id,
               company_id=new_company.company_id,
          )
          db.session.execute(UserCompany)
          db.session.commit()

          return {"mensagem": "Empresa cadastrada com sucesso",
               "company_id": new_company.company_id,
               "name": new_company.name,
               "cnpj": new_company.cnpj}, 201
     
     except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar empresa: {str(e)}")
        return {"erro": f"Ocorreu um erro interno ao tentar cadastrar a empresa: {str(e)}"}, 500

def find_company(company_CNPJ,user_id):
     if not company_CNPJ:
          return None
     return db.session.query(Company).filter(Company.cnpj==company_CNPJ).first()

def delete_company(company_id, user_id):
     try:
          company = CompanyRepository.get_by_id(company_id)
          if not company:
               raise APIException("Empresa não encontrada.", 404)
          
          CompanyRepository.check_access(company_id, user_id)
          CompanyRepository.delete(company_id)
          
          return {"mensagem": "Empresa deletada com sucesso."}, 200
     
     except APIException as ve:
          raise ve
     except Exception as e:
          db.session.rollback()
          print(f"Erro ao deletar empresa: {str(e)}")
          return {"erro": f"Ocorreu um erro interno ao tentar deletar a empresa: {str(e)}"}, 500

def update_company(cnpj, data, user_id):

    cnpj_clean = re.sub(r'\D', '', cnpj)
    company = find_company(cnpj_clean)

    if not company:
        return {"erro": "Empresa não encontrada."}, 404

    has_access = db.session.query(user_company).filter(
        user_company.c.user_id == user_id,
        user_company.c.company_id == company.company_id
    ).first()

    if not has_access:
        return {"erro": "Acesso negado. Você não tem permissão para alterar esta empresa."}, 403

    novo_cnpj = data.get('cnpj')
    if novo_cnpj:
        novo_cnpj_clean = re.sub(r'\D', '', novo_cnpj)
        if novo_cnpj_clean != company.cnpj:
            # Reutiliza o find_company para ver se o novo CNPJ já existe no banco
            if find_company(novo_cnpj_clean):
                return {"erro": "Este CNPJ já está em uso por outra empresa."}, 409
            company.cnpj = novo_cnpj_clean

    if 'name' in data:
        company.name = data['name']

    try:
        db.session.commit()
        return {"mensagem": "Dados da empresa atualizados com sucesso."}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao tentar atualizar a empresa."}, 500