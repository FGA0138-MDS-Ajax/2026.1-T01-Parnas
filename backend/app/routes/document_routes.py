from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.services.document_service import DocumentService
from app.schemas.document_schema import DocumentUploadSchema, DocumentResponseSchema

document_bp = Blueprint('document_dp', __name__)

@document_bp.route('', methods=['POST'])
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
        'company_id':  request.form.get('company_id'),
    }

    try:
        if raw_data['company_id'] is not None:
            raw_data['company_id'] = int(raw_data['company_id'])
    except (ValueError, TypeError):
        return jsonify({"erro": "company_id deve ser um número inteiro"}), 400

    try:
        validated = DocumentUploadSchema().load(raw_data)
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    document, error, status_code = DocumentService.save_document(
        file=file,
        user_id=current_user_id,
        company_id=validated['company_id'],
        name=validated['name'],
        tipo=validated['type'],
        description=validated.get('description')
    )

    if error:
        return jsonify({"erro": error}), status_code

    return jsonify(DocumentResponseSchema().dump(document)), status_code


@document_bp.route('', methods=['GET'])
@jwt_required()
def get_documents():
    current_user_id = int(get_jwt_identity())

    company_id = request.args.get('company_id', type=int)
    if not company_id:
        return jsonify({"erro": "Parâmetro 'company_id' é obrigatório"}), 400

    tipo     = request.args.get('type')
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination, error, status_code = DocumentService.get_documents_by_company(
        company_id=company_id,
        user_id=current_user_id,
        tipo=tipo,
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
    pass

@document_bp.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    pass