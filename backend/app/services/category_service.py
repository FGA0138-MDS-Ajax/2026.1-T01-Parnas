from app.repositories.category_repository import CategoryRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.exceptions.api_exception import APIException



def add_category(user_id, company_id, data):
    company = CompanyRepository.get_by_id(company_id)
    if not company:
        raise APIException("Empresa não encontrada.", 404)

    access = CompanyRepository.check_user_access(company_id, user_id)
    if not access:
        raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
    
    try:
        new_category = CategoryRepository.create(
            name=data.get("name"),
            type=data.get("type"),
            company_id=company_id
        )
        return {"category": new_category}, 201
    except Exception as e:
        return {"erro": f"Erro interno ao salvar a categoria: {str(e)}"}, 500


def get_categories(user_id, company_id):
    access = CompanyRepository.check_user_access(company_id, user_id)
    if not access:
        raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

    categories = CategoryRepository.list_by_company(company_id)
    return {"categories": categories}, 200


def update_category(user_id, company_id, category_id, data):
    access = CompanyRepository.check_user_access(company_id, user_id)
    if not access:
        raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

    category = CategoryRepository.get_by_id_and_company(category_id, company_id)
    if not category:
        raise APIException("Categoria não encontrada para esta empresa.", 404)

    # update() sobrescreve sempre, então preenche com o valor atual se não vier no data
    new_name = data.get("name", category.name)
    new_type = data.get("type", category.type)

    try:
        updated = CategoryRepository.update(category_id, company_id, new_name, new_type)
        return {"category": updated}, 200
    except Exception as e:
        return {"erro": f"Erro interno ao atualizar: {str(e)}"}, 500


def delete_category(user_id, company_id, category_id):
    try:
        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

        success = CategoryRepository.delete(category_id, company_id)
        if not success:
            raise APIException("Categoria não encontrada para esta empresa.", 404)
        return {"msg": "Categoria deletada com sucesso!"}, 200
    
    except APIException as ve:
        raise ve
    except Exception as e:
        return {"erro": f"Erro interno ao deletar: {str(e)}"}, 500