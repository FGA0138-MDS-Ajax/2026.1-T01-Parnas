from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository


def _user_has_access(user_id, company_id):
    user = UserRepository.get_by_id(user_id)
    if not user:
        return False
    return any(c.company_id == company_id for c in user.companies)


def add_category(user_id, company_id, data):
    if not _user_has_access(user_id, company_id):
        return {"erro": "Usuário não tem acesso a esta empresa."}, 403

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
    if not _user_has_access(user_id, company_id):
        return {"erro": "Usuário não tem acesso a esta empresa."}, 403

    categories = CategoryRepository.list_by_company(company_id)
    return {"categories": categories}, 200


def update_category(user_id, company_id, category_id, data):
    if not _user_has_access(user_id, company_id):
        return {"erro": "Usuário não tem acesso a esta empresa."}, 403

    category = CategoryRepository.get_by_id_and_company(category_id, company_id)
    if not category:
        return {"erro": "Categoria não encontrada para esta empresa."}, 404

    # update() sobrescreve sempre, então preenche com o valor atual se não vier no data
    new_name = data.get("name", category.name)
    new_type = data.get("type", category.type)

    try:
        updated = CategoryRepository.update(category_id, company_id, new_name, new_type)
        return {"category": updated}, 200
    except Exception as e:
        return {"erro": f"Erro interno ao atualizar: {str(e)}"}, 500


def delete_category(user_id, company_id, category_id):
    if not _user_has_access(user_id, company_id):
        return {"erro": "Usuário não tem acesso a esta empresa."}, 403

    success = CategoryRepository.delete(category_id, company_id)
    if not success:
        return {"erro": "Categoria não encontrada para esta empresa."}, 404

    return {"msg": "Categoria deletada com sucesso!"}, 200