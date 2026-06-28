from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.services.document_service import DocumentService
from app.schemas.document_schema import DocumentUploadSchema, DocumentResponseSchema

document_bp = Blueprint('document_bp', __name__)


@document_bp.route('/', methods=['POST'])
@jwt_required()
def upload_document():
    current_user_id = int(get_jwt_identity())
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado. Use multipart/form-data com o campo 'file'"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    raw_data = {
        'name':        request.form.get('name'),
        'type':        request.form.get('type'),
        'description': request.form.get('description'),
    }
    try:
        validated = DocumentUploadSchema().load(raw_data)
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400
    document, error, status_code = DocumentService.save_document(
        file=file,
        user_id=current_user_id,
        name=validated['name'],
        tipo=validated['type'],
        description=validated.get('description')
    )
    if error:
        return jsonify({"erro": error}), status_code
    return jsonify(DocumentResponseSchema().dump(document)), status_code


@document_bp.route('/', methods=['GET'])
@jwt_required()
def get_documents():
    current_user_id = int(get_jwt_identity())
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    pagination, error, status_code = DocumentService.get_documents_by_company(
        user_id=current_user_id,
        page=page,
        per_page=per_page
    )
    if error:
        return jsonify({"erro": error}), status_code
    return jsonify({
        "documentos":   DocumentResponseSchema(many=True).dump(pagination.items),
        "total":        pagination.total,
        "paginas":      pagination.pages,
        "pagina_atual": pagination.page,
        "por_pagina":   pagination.per_page,
    }), status_code


@document_bp.route('/<int:document_id>/download', methods=['GET'])
@jwt_required()
def download_document(document_id):
    current_user_id = int(get_jwt_identity())
    file_path, download_name, error, status_code = DocumentService.get_document_for_download(
        document_id=document_id,
        user_id=current_user_id
    )
    if error:
        return jsonify({"erro": error}), status_code
    return send_file(
        file_path,
        as_attachment=True,
        download_name=download_name
    )


@document_bp.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    current_user_id = int(get_jwt_identity())
    success, message, status_code = DocumentService.delete_document(
        document_id=document_id,
        user_id=current_user_id
    )
    key = "mensagem" if success else "erro"
    return jsonify({key: message}), status_code