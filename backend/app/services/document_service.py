import os
from datetime import datetime, date
from werkzeug.utils import secure_filename
from app.config import Config
from app.repositories.document_repository import DocumentRepository
from app.repositories.company_repository import CompanyRepository
from app.exceptions import APIException

class DocumentService:
    ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS
    ALLOWED_TYPES = Config.ALLOWED_DOCUMENT_TYPES
    MAX_SIZE = Config.MAX_CONTENT_LENGTH
    UPLOAD_FOLDER = Config.UPLOAD_FOLDER

    @staticmethod
    def validate_file_extension(filename):
        if not filename or '.' not in filename:
            return False, "Arquivo sem extensão válida"

        extension = filename.rsplit('.', 1)[1].lower()

        if extension not in DocumentService.ALLOWED_EXTENSIONS:
            allowed = ', '.join(DocumentService.ALLOWED_EXTENSIONS)
            return False, f"Tipo de arquivo não permitido. Permitidos: {allowed}"

        return True, None


    @staticmethod
    def validate_file_size(file):
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        max_mb = DocumentService.MAX_SIZE / (1024 * 1024)
        if file_size > DocumentService.MAX_SIZE:
            return False, f"Arquivo muito grande. Máximo: {max_mb:.0f}MB"

        return True, None


    @staticmethod
    def save_document(file, user_id, company_id, name, tipo, description=None):
        try:
            if not company_id:
                return None, "Nenhuma empresa selecionada.", 400
            
            if not CompanyRepository.check_user_access(company_id, user_id):
                return None, "Acesso negado a esta empresa corporativa.", 403

            if not file or file.filename == '':
                return None, "Arquivo não selecionado", 400

            valid, msg = DocumentService.validate_file_extension(file.filename)
            if not valid:
                return None, msg, 400

            valid, msg = DocumentService.validate_file_size(file)
            if not valid:
                return None, msg, 400

            company_folder = os.path.join(DocumentService.UPLOAD_FOLDER, str(company_id))
            os.makedirs(company_folder, exist_ok=True)

            filename = secure_filename(file.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
            unique_filename = timestamp + filename
            filepath = os.path.join(company_folder, unique_filename)

            file.save(filepath)
            file_size = os.path.getsize(filepath)

            data = {
                'company_id': company_id,
                'user_id': user_id,
                'name': name,
                'type': tipo,
                'description': description,
                'file_path': filepath,
                'size': file_size,
                'created_at': date.today()
            }

            document = DocumentRepository.create(data)
            return document, None, 201

        except Exception as e:
            return None, f"Erro ao salvar documento: {str(e)}", 500


    @staticmethod
    def get_documents_by_company(user_id, company_id, page=1, per_page=20):
        try:
            if not company_id:
                return None, "Nenhuma empresa selecionada.", 400

            if not CompanyRepository.check_user_access(company_id, user_id):
                return None, "Acesso negado a esta empresa corporativa.", 403

            query = DocumentRepository.get_by_company(company_id, page, per_page)
            return query, None, 200

        except Exception as e:
            return  {"erro": f"Erro ao listar documentos: {str(e)}"}, 500


    @staticmethod
    def delete_document(document_id, user_id, company_id):
        try:
            if not company_id:
                return False, "Nenhuma empresa selecionada.", 400

            if not CompanyRepository.check_user_access(company_id, user_id):
                return False, "Acesso negado a esta empresa corporativa.", 403

            document = DocumentRepository.get_by_id_and_company(document_id, company_id)
            if not document:
                return False, "Documento não encontrado", 404

            if os.path.exists(document.file_path):
                os.remove(document.file_path)

            DocumentRepository.delete(document)
            return True, "Documento deletado com sucesso", 200

        except Exception as e:
            return {"erro": f"Erro ao deletar documento: {str(e)}"}, 500

    @staticmethod
    def get_document_for_download(document_id, user_id, company_id):
        try:
            if not company_id:
                return None, None, "Nenhuma empresa selecionada.", 400

            if not CompanyRepository.check_user_access(company_id, user_id):
                return None, None, "Acesso negado a esta empresa corporativa.", 403

            document = DocumentRepository.get_by_id_and_company(document_id, company_id)
            if not document:
                raise APIException("Documento não encontrado", 404)

            document_path = os.path.exists(document.file_path)
            if not document_path:
                raise APIException("Arquivo não encontrado no servidor", 404)

            extension = os.path.splitext(document.file_path)[1]
            download_name = secure_filename(document.name) + extension
            return {"file_path": document.file_path, "download_name": download_name}, 200
        
        except APIException as ve:
            raise ve
        except Exception as e:
            return {"erro": f"Erro ao buscar documento para download: {str(e)}"}, 500