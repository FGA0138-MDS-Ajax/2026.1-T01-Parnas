from app.models.document import Document
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository):
    
    _base = BaseRepository(Document)
    
    @staticmethod
    def create(data):
        document = Document(**data)
        return DocumentRepository._base.save(document)
    
    @staticmethod
    def get_by_company(company_id, page=1, per_page=20):
        return Document.query.filter_by(company_id=company_id)\
            .order_by(Document.created_at.desc())\
            .paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_by_id_and_company(document_id, company_id):
        return Document.query.filter_by(
            document_id=document_id, 
            company_id=company_id
        ).first()
    
    @staticmethod
    def delete(document):
        DocumentRepository._base.delete(document)
        return True