import os
from app.config import Config

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