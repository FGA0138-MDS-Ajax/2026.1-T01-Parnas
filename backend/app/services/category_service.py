from app.repositories.category_repository import CategoryRepository
from app.repositories.company_repository import CompanyRepository

def add_category(user_id, data):
    cnpj = data.get("cnpj")

    company = CompanyRepository.get_by_cnpj(cnpj)
    if not company:
        return {"erro": "Empresa não encontrada ou você não tem permissão para gerenciar as categorias dela."}, 404

    try:
        # Criando via Repository
        CategoryRepository.create(
            name=data.get("name"),
            type=data.get("type"),
            company_id=company.company_id
        )
        return {"msg": "Categoria criada com sucesso!"}, 201
    except Exception as e:
        return {"erro": f"Erro interno ao salvar a categoria: {str(e)}"}, 500

def get_categories(user_id, data):
    cnpj = data.get("cnpj")

    company = CompanyRepository.get_by_cnpj(cnpj)
    if not company:
        return {"erro": "Empresa não encontrada ou você não tem permissão."}, 404

    categories = CategoryRepository.list_by_company(company.company_id)
    return {"categories": categories}, 200

def update_category(user_id, data):
    category_id = data.get("category_id") or data.get("id")
    cnpj = data.get("cnpj")

    company = CompanyRepository.get_by_cnpj(cnpj)
    if not company:
        return {"erro": "Empresa não encontrada ou você não tem permissão."}, 404

    category = CategoryRepository.get_by_id_and_company(category_id, company.company_id)
    if not category:
        return {"erro": "Categoria não encontrada para esta empresa."}, 404

    if "name" in data:
        category.name = data.get("name")
    if "type" in data:
        category.type = data.get("type")

    try:
        from app.config import db
        db.session.commit()
        return {"msg": "Categoria actualizada com sucesso!"}, 200
    except Exception as e:
        return {"erro": f"Erro interno ao atualizar: {str(e)}"}, 500

def delete_category(user_id, data):
    category_id = data.get("category_id") or data.get("id")
    cnpj = data.get("cnpj")

    company = CompanyRepository.get_by_cnpj(cnpj)
    if not company:
        return {"erro": "Empresa não encontrada ou você não tem permissão."}, 404

    deleted = CategoryRepository.delete(category_id, company.company_id)
    if not deleted:
        return {"erro": "Categoria não encontrada para esta empresa."}, 404

    return {"msg": "Categoria deletada com sucesso!"}, 200