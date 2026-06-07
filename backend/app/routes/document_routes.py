from flask import Blueprint
from flask_jwt_extended import jwt_required

document_bp = Blueprint('document_dp', __name__)

@document_bp.route('', methods=['POST'])
@jwt_required()
def upload_document():
    pass

@document_bp.route('', methods=['GET'])
@jwt_required()
def get_documents():
    pass

@document_bp.route('/<int:document_id>/download', methods=['GET'])
@jwt_required()
def download_document(document_id):
    pass

@document_bp.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    pass