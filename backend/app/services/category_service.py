from app.models import Category, Company 
from app.config import db
from flask_jwt_extended import get_jwt


def add_category(data):
    claims = get_jwt()
    company_id = claims.get("active_company_id")

    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    new_category = Category(
        name=data.get("name"),
        type=data.get("type"),
        company_id=company_id
    )

    try:
        db.session.add(new_category)
        db.session.commit()
        return {"msg": "Categoria criada com sucesso!"}, 201
    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro interno ao salvar a categoria: {str(e)}"}, 500


def get_categories():
    claims = get_jwt()
    company_id = claims.get("active_company_id")

    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    categories = Category.query.filter_by(company_id=company_id).all()
    return {"categories": categories}, 200


def update_category(data):
    category_id = data.get("category_id") or data.get("id")
    claims = get_jwt()
    company_id = claims.get("active_company_id")

    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    category = Category.query.filter_by(category_id=category_id, company_id=company_id).first()
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


def delete_category(data):
    category_id = data.get("category_id") or data.get("id")
    claims = get_jwt()
    company_id = claims.get("active_company_id")

    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    category = Category.query.filter_by(category_id=category_id, company_id=company_id).first()
    if not category:
        return {"erro": "Categoria não encontrada para esta empresa."}, 404

    try:
        db.session.delete(category)
        db.session.commit()
        return {"msg": "Categoria deletada com sucesso!"}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro interno ao deletar: {str(e)}"}, 500