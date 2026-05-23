from marshmallow import Schema, fields, validate, ValidationError, pre_load
from app.utils.validators import is_valid_cnpj

class CompanyRegistrationSchema(Schema):
    name = fields.String(
          required=True,
          validate=validate.Length(min=1, max=150),
          error_messages={"required": "Nome é obrigatório","invalid": "Nome deve ser uma string"}
     )
    cnpj = fields.String(
        required=True,
        validate=validate.Length(min=14, max=20),
        error_messages={"required": "CNPJ é obrigatório","validator_failed": "CNPJ inválido"}
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
    
    @pre_load
    def validate_cnpj_format(self, data, **kwargs):
        if 'cnpj' in data:
            is_valid, error_msg = is_valid_cnpj(data['cnpj'])
            if not is_valid:
                raise ValidationError({"cnpj": error_msg})
        return data