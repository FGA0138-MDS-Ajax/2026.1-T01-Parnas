from app.repositories import CategoryRepository, CompanyRepository
from app.config import db
from app.exceptions.api_exception import APIException


def add_category(user_id, company_id, data):

    company = CompanyRepository.get_by_id(company_id)
    if not company:
        raise APIException("Empresa não encontrada", 404)
    
    access = CompanyRepository.check_user_permission(company_id, user_id)
    if not access:
        raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
      
    try:
        new_category = CategoryRepository.create(
            name=data.get("name"),
            type=data.get("type"),
            company_id=company_id
        )
        
        return {"msg": "Categoria criada com sucesso!", "category": new_category}, 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar categoria: {str(e)}")
        return {"erro": f"Erro interno ao salvar a categoria: {str(e)}"}, 500


def get_categories(user_id, company_id):

    company = CompanyRepository.get_by_id(company_id)
    if not company:
        raise APIException("Empresa não encontrada", 404)
    
    access = CompanyRepository.check_user_permission(company_id, user_id)
    if not access:
        raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
    
    try:
        categories = CategoryRepository.list_by_company(company_id)  
        return {"categories": categories}, 200
                           
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao acessar categorias: {str(e)}")
        return {"erro": f"Erro interno ao acessar a categorias: {str(e)}"}, 500

def update_category(user_id, company_id, category_id, data):
    company = CompanyRepository.get_by_id(company_id)
    if not company:
        raise APIException("Empresa não encontrada", 404)
           
    access = CompanyRepository.check_user_permission(company_id, user_id)
    if not access:
        raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
                           
    category = CategoryRepository.get_by_id_and_company(category_id, company_id)
    if not category:
        raise APIException("Categoria não encontrada para esta empresa.", 404)
    
    if not data.get("name") or not data.get("type"):
        raise APIException("Nome e tipo são obrigatórios.", 400)
    
    new_name = data.get("name")
    new_type = data.get("type")

    try:
        updated_category = CategoryRepository.update(
            category_id=category_id,
            company_id=company_id,
            new_name=new_name,
            new_type=new_type
        )
        db.session.commit()
                           
        return {"msg": "Categoria atualizada com sucesso!", "category": updated_category}, 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar categoria: {str(e)}")
        return {"erro": f"Erro interno ao atualizar categoria: {str(e)}"}, 500

def delete_category(user_id, company_id, category_id):
                           
    company = CompanyRepository.get_by_id(company_id)
    if not company:
        raise APIException("Empresa não encontrada", 404)
    
    access = CompanyRepository.check_user_permission(company_id, user_id)
    if not access:
        raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
                           
    category = CategoryRepository.get_by_id_and_company(category_id, company_id)
    if not category:
        raise APIException("Categoria não encontrada para esta empresa.", 404)
                           
    try:
        deleted = CategoryRepository.delete(category_id, company_id)
        return {"msg": "Categoria deletada com sucesso!", "deleted":deleted}, 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar categoria: {str(e)}")
        return {"erro": f"Erro interno ao deletar: {str(e)}"}, 500
