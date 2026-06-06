from app.config import db
from app.models.document import Document

class DocumentRepository:

    @staticmethod
    def create(data):
        """Salva um novo documento no banco e retorna a instância criada."""
        document = Document(**data)
        db.session.add(document)
        db.session.commit()
        return document

    @staticmethod
    def get_by_company(company_id, page=1, per_page=20):
        """Lista documentos paginados por empresa, ordenados do mais recente."""
        return Document.query.filter_by(company_id=company_id)\
            .order_by(Document.created_at.desc())\
            .paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id_and_company(document_id, company_id):
        """Busca um documento específico garantindo que ele pertence à empresa."""
        return Document.query.filter_by(
            document_id=document_id, 
            company_id=company_id
        ).first()

    @staticmethod
    def delete(document):
        """Remove o registro do banco de dados."""
        db.session.delete(document)
        db.session.commit()
        return True