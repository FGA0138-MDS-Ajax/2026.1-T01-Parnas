from marshmallow import Schema, fields, validate, ValidationError, validates
from validate_docbr import CNPJ

class CategoryAddSchema(Schema):
    id = fields.Int(load_only=True)
    type = fields.String(
        required=True,
        validate=validate.Length(min=1, max=20),
        error_messages={"required": "Tipo é obrigatório"}
    )
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Nome é obrigatório"}
    )
    cnpj = fields.String(
        required=True,
        error_messages={"required": "CNPJ é obrigatório"}
    )

    @validates('cnpj')
    def validate_cnpj_format(self, value, **kwargs):
        cnpj_validator = CNPJ()
        if not cnpj_validator.validate(value):
            raise ValidationError("CNPJ inválido")
    
class CategoryRequirements(Schema):
    id = fields.Int(dump_only=True)    
    type = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    cnpj = fields.Str(dump_only=True)