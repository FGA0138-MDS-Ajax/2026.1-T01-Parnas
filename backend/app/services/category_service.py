from app.models import Category, Company 
from app.repositories.category_repository import CategoryRepository
from app.repositories.company_repository import CompanyRepository
from app.exceptions.api_exception import APIException
from app.config import db


def add_category(user_id, company_id, data):

    company = CompanyRepository.get_by_id(company_id)
    if not company:
        raise APIException("Empresa não encontrada", 404)
    
    CompanyRepository.check_user_permission(company_id, user_id)

    name = data.get("name")
    type = data.get("type")

    try:
        new_category = CategoryRepository.create(
            name=name,
            type=type,
            company_id=company_id
        )
        CategoryRepository.create(new_category)
        return {"msg": "Categoria criada com sucesso!", "category": new_category}, 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar categoria: {str(e)}")
        return {"erro": f"Erro interno ao salvar a categoria: {str(e)}"}, 500


def get_categories(user_id, data):
    cnpj = data.get("cnpj")

    company = Company.query.filter_by(cnpj=cnpj).first()
    if not company:
        return {"erro": "Empresa não encontrada ou você não tem permissão."}, 404

    categories = Category.query.filter_by(company_id=company.company_id).all()
    return {"categories": categories}, 200


def update_category(user_id, data):
    category_id = data.get("category_id") or data.get("id")
    cnpj = data.get("cnpj")

    company = Company.query.filter_by(cnpj=cnpj).first()
    if not company:
        return {"erro": "Empresa não encontrada ou você não tem permissão."}, 404

    category = Category.query.filter_by(category_id=category_id, company_id=company.company_id).first()
    if not category:
        return {"erro": "Categoria não encontrada para esta empresa."}, 404

    if "name" in data:
        category.name = data.get("name")
    if "type" in data:
        category.type = data.get("type")

    try:
        db.session.commit()
        return {"msg": "Categoria actualizada com sucesso!"}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro interno ao atualizar: {str(e)}"}, 500


def delete_category(user_id, data):
    category_id = data.get("category_id") or data.get("id")
    cnpj = data.get("cnpj")

    company = Company.query.filter_by(cnpj=cnpj).first()
    if not company:
        return {"erro": "Empresa não encontrada ou você não tem permissão."}, 404

    category = Category.query.filter_by(category_id=category_id, company_id=company.company_id).first()
    if not category:
        return {"erro": "Categoria não encontrada para esta empresa."}, 404

    try:
        db.session.delete(category)
        db.session.commit()
        return {"msg": "Categoria deletada com sucesso!"}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro interno ao deletar: {str(e)}"}, 500