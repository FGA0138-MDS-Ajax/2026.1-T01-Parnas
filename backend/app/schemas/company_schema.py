from marshmallow import Schema, fields, validate, ValidationError, validates
from validate_docbr import CNPJ

class CompanyRegistrationSchema(Schema):
    name = fields.String(
          required=True,
          validate=validate.Length(min=1, max=150),
          error_messages={"required": "Nome é obrigatório","invalid": "Nome deve ser uma string"}
     )
    cnpj = fields.String(
        required=True,
        error_messages={"required": "CNPJ é obrigatório"}
    )
    email = fields.Email(
        required=True,
        error_messages={"required": "Email é obrigatório","invalid": "Email inválido"}
    )
    phone = fields.String(
        required=True,
        validate=validate.Length(min=8, max=20),
        error_messages={"required": "Telefone é obrigatório","validator_failed": "Telefone deve ter entre 8 e 20 caracteres"}
    )
    @validates('cnpj')
    def validate_cnpj_format(self, value, **kwargs):
        cnpj_validator = CNPJ()
        if not cnpj_validator.validate(value):
            raise ValidationError("CNPJ inválido")

class CompanyDeleteSchema(Schema):
    cnpj = fields.String(
        required=True,
        error_messages={"required": "CNPJ é obrigatório"}
    )
    @validates('cnpj')
    def validate_cnpj_format(self, value, **kwargs):
        cnpj_validator = CNPJ()
        if not cnpj_validator.validate(value):
            raise ValidationError("CNPJ inválido")