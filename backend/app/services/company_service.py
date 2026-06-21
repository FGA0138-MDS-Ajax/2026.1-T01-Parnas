from app.models.company import Company
from app.config import db
from app.repositories.company_repository import CompanyRepository
from app.exceptions.api_exception import APIException

def register_company(user_id, data):
     try:
          name = data.get('name')
          cnpj = data.get('cnpj')
          email = data.get('email')
          phone = data.get('phone')
          
          if(CompanyRepository.get_by_cnpj(cnpj)):
               raise APIException("CNPJ já cadastrado.", 409)
          
          new_company = CompanyRepository.create(name, cnpj, email, phone, user_id)

          return {"mensagem": "Empresa cadastrada com sucesso",
               "company_id": new_company.company_id,
               "name": new_company.name,
               "cnpj": new_company.cnpj}, 201
     
     except APIException as ve:
          raise ve
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

def update_company(data, user_id, company_id):
     try:
          company = CompanyRepository.get_by_id(company_id)
          if not company:
               raise APIException("Empresa não encontrada.", 404)
          
          CompanyRepository.check_access(company_id, user_id)

          if 'cnpj' in data:
               if(CompanyRepository.get_by_cnpj(data['cnpj']) and CompanyRepository.get_by_cnpj(data['cnpj']).company_id != company_id):
                    raise APIException("CNPJ já cadastrado.", 409)
               company.cnpj = data['cnpj']
          if 'name' in data:
               company.name = data['name']
          if 'email' in data:
               company.email = data['email']
          if 'phone' in data:
               company.phone = data['phone']
          db.session.commit()

          return {"mensagem": "Dados da empresa atualizados com sucesso.", "company": company}, 200
          
     except APIException as ve:
          raise ve
     except Exception as e:
          db.session.rollback()
          print(f"Erro ao atualizar empresa: {str(e)}")
          return {"erro": f"Ocorreu um erro interno ao tentar atualizar a empresa: {str(e)}"}, 500