from marshmallow import Schema, fields, validates, ValidationError
from app.utils.validators import is_valid_password, is_valid_birth_date

class UserRegistrationSchema(Schema):
    name = fields.Str(required=True, error_messages={"required": "Nome é obrigatório."})
    email = fields.Email(required=True, error_messages={"required": "E-mail é obrigatório.",
    "invalid": "Formato de e-mail inválido."})
    cpf = fields.Str(required=True, error_messages={"required": "O CPF é obrigatório."})
    password = fields.Str(required=True, error_messages={"required": "A senha é obrigatória."})
    birth_date = fields.Str(required=True, error_messages={"required": "A data de nascimento é obrigatória"})

    @validates('password')
    def validate_password(self, value):
        if not is_valid_password(value):
            raise ValidationError("A senha não atende aos requisitos mínimos de segurança.")

    @validates('birth_date')
    def validate_birth_date(self, value):
        if not is_valid_birth_date(value):
            raise ValidationError("A data de nascimento é invalida ou o usuário é menor de 16 anos.")