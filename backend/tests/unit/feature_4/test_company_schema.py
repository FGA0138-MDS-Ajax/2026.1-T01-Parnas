from marshmallow import ValidationError

from app.schemas.company_schema import CompanyRegistrationSchema


def test_company_schema_requires_name():
    schema = CompanyRegistrationSchema()

    try:
        schema.load({
            "cnpj": "04.252.011/0001-10",
            "email": "empresa@teste.com",
            "phone": "11999999999",
        })
        assert False, "ValidationError era esperado"
    except ValidationError as err:
        assert "name" in err.messages
        assert err.messages["name"][0] == "Nome é obrigatório"


def test_company_schema_requires_cnpj():
    schema = CompanyRegistrationSchema()

    try:
        schema.load({
            "name": "Empresa de Teste LTDA",
            "email": "empresa@teste.com",
            "phone": "11999999999",
        })
        assert False, "ValidationError era esperado"
    except ValidationError as err:
        assert "cnpj" in err.messages
        assert err.messages["cnpj"][0] == "CNPJ é obrigatório"


def test_company_schema_rejects_invalid_cnpj():
    schema = CompanyRegistrationSchema()

    try:
        schema.load({
            "name": "Empresa de Teste LTDA",
            "cnpj": "11.111.111/1111-11",
            "email": "empresa@teste.com",
            "phone": "11999999999",
        })
        assert False, "ValidationError era esperado"
    except ValidationError as err:
        assert "cnpj" in err.messages
        assert err.messages["cnpj"][0] == "CNPJ inválido"
