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
    def get_by_company(id_empresa, page=1, per_page=20):
        """Lista documentos paginados por empresa, ordenados do mais recente."""
        return Document.query.filter_by(id_empresa=id_empresa)\
            .order_by(Document.data_upload.desc())\
            .paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id_and_company(id_documento, id_empresa):
        """Busca um documento específico garantindo que ele pertence à empresa."""
        return Document.query.filter_by(
            id_documento=id_documento, 
            id_empresa=id_empresa
        ).first()

    @staticmethod
    def delete(documento):
        """Remove o registro do banco de dados."""
        db.session.delete(documento)
        db.session.commit()
        return True