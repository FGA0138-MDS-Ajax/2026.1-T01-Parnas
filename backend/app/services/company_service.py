import re
from app.config import db
from datetime import date
from app.exceptions.api_exception import APIException
from app.repositories.company_repository import CompanyRepository


def register_company(user_id, data):
     try:
          name = data.get('name')
          cnpj = data.get('cnpj')
          email = data.get('email')
          phone = data.get('phone')

          cnpj_clean = re.sub(r'\D', '', cnpj)
          if CompanyRepository.get_by_cnpj(cnpj_clean):
              raise APIException("CNPJ já cadastrado.", 409)
            
          new_company = CompanyRepository.create(
              name=name,
              cnpj=cnpj_clean,
              email=email,
              phone=phone,
              register_date=date.today()
          )
          
          CompanyRepository.attach_user(new_company.company_id, user_id)

          return {
               "mensagem": "Empresa cadastrada com sucesso",
               "company_id": new_company.company_id,
               "name": new_company.name,
               "cnpj": new_company.cnpj
          }, 201
     
     except APIException as ve:
          raise ve
     except Exception as e:
          db.session.rollback()
          print(f"Erro ao cadastrar empresa: {str(e)}")
          return {"erro": f"Ocorreu um erro interno ao tentar cadastrar a empresa: {str(e)}"}, 500
        
        
def delete_company(company_id, user_id):
     try:
          company = CompanyRepository.get_by_id(company_id)
          if not company:
               raise APIException("Empresa não encontrada.", 404)
          
          access = CompanyRepository.check_user_access(company_id, user_id)
          if not access:
               raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
                                  
          CompanyRepository.delete(company)
          
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
          
          access = CompanyRepository.check_user_access(company_id, user_id)
          if not access:
               raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

          if 'cnpj' in data:
               cnpj_clean = re.sub(r'\D', '', data['cnpj'])
               if(CompanyRepository.get_by_cnpj(cnpj_clean) and CompanyRepository.get_by_cnpj(cnpj_clean).company_id != company_id):
                    raise APIException("CNPJ já cadastrado.", 409)
               company.cnpj = cnpj_clean
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
     
                                  
def get_company(company_id, user_id):
     try:
          company = CompanyRepository.get_by_id(company_id)
          if not company:
              raise APIException("Empresa não encontrada.", 404)

          access = CompanyRepository.check_user_access(company_id, user_id)
          if not access:
              raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

          return {"company": company}, 200
                                 
     except APIException as ve:
          raise ve
     except Exception as e:
          print(f"Erro ao buscar empresa: {str(e)}")
          return {"erro": f"Ocorreu um erro interno ao tentar buscar a empresa: {str(e)}"}, 500
     
                                 
def get_all_companies(user_id):
     try:
          companies = CompanyRepository.get_all_by_user(user_id)
          return {"companies": companies}, 200
     
     except Exception as e:
          print(f"Erro ao buscar empresas: {str(e)}")
          return {"erro": f"Ocorreu um erro interno ao tentar buscar as empresas: {str(e)}"}, 500
