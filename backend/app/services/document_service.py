import os
from werkzeug.utils import secure_filename
from datetime import date
from app.config import db, Config
from app.models.company import Company
from app.models.user import User
from app.repositories.document_repository import DocumentRepository

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
    def check_user_company_access(user_id, company_id):
        user = User.query.get(user_id)
        if not user:
            return False, "Usuário não encontrado", 404
        
        company = Company.query.get(company_id)
        if not company:
            return False, "Empresa não encontrada", 404
        
        if company not in user.companies:
            return False, "Você não tem acesso a esta empresa", 403
        
        return True, None, None

    @staticmethod
    def save_document(file, user_id, company_id, name, tipo, description=None):
        try:
            if not file or file.filename == '':
                return None, "Arquivo não selecionado", 400
            
            valid, msg = DocumentService.validate_file_extension(file.filename)
            if not valid:
                return None, msg, 400
            
            valid, msg = DocumentService.validate_file_size(file)
            if not valid:
                return None, msg, 400
            
            has_access, error_msg, status_code = DocumentService.check_user_company_access(user_id, company_id)
            if not has_access:
                return None, error_msg, status_code
            
            company_folder = os.path.join(DocumentService.UPLOAD_FOLDER, str(company_id))
            os.makedirs(company_folder, exist_ok=True)
            
            filename = secure_filename(file.filename)
            from datetime import datetime
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
            db.session.rollback()
            return None, f"Erro ao salvar documento: {str(e)}", 500