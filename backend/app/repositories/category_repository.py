from app.config import db
from app.models.category import Category

class CategoryRepository:
    
    @staticmethod
    def list_by_company(company_id):
        """Lista todas as categorias vinculadas a uma empresa específica."""
        return Category.query.filter_by(company_id=company_id).all()

    @staticmethod
    def get_by_id_and_company(category_id, company_id):
        """Busca uma categoria específica garantindo que pertence à empresa."""
        return Category.query.filter_by(
            category_id=category_id, 
            company_id=company_id
        ).first()

    @staticmethod
    def create(name, type, company_id):
        """Cria uma nova categoria para a empresa."""
        new_category = Category(name=name, type=type, company_id=company_id)
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def update(category_id, company_id, new_name):
        """Edita o nome de uma categoria existente."""
        category = CategoryRepository.get_by_id_and_company(category_id, company_id)
        if category:
            category.name = new_name
            db.session.commit()
        return category

    @staticmethod
    def delete(category_id, company_id):
        """Exclui uma categoria da empresa."""
        category = CategoryRepository.get_by_id_and_company(category_id, company_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False