from marshmallow import Schema, fields, validate


class DocumentUploadSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={"required": "Nome do documento é obrigatório"}
    )
    type = fields.Str(
        required=True,
        validate=validate.OneOf(['fiscal', 'contabil', 'juridico']),
        error_messages={"required": "Tipo de documento é obrigatório",
                       "validator_failed": "Tipo deve ser: fiscal, contabil ou juridico"}
    )
    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=500)
    )


class DocumentResponseSchema(Schema):
    document_id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    description = fields.Str()
    size = fields.Int()
    created_at = fields.Date()