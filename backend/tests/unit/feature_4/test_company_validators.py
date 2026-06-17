import pytest
from marshmallow import ValidationError
from app.schemas.category_schema import CategoryAddSchema


@pytest.fixture
def schema():
    return CategoryAddSchema()


def test_schema_accepts_known_valid_cnpj(schema):
    payload = {"cnpj": "04.252.011/0001-10"}

    result = schema.load(payload, partial=True)

    assert result["cnpj"] == "04.252.011/0001-10"


def test_schema_rejects_cnpj_with_wrong_length(schema):
    payload = {"cnpj": "123"}

    with pytest.raises(ValidationError) as exc_info:
        schema.load(payload, partial=True)

    assert "CNPJ inválido" in exc_info.value.messages["cnpj"]


def test_schema_rejects_cnpj_with_invalid_check_digits(schema):
    payload = {"cnpj": "11.111.111/1111-11"}

    with pytest.raises(ValidationError) as exc_info:
        schema.load(payload, partial=True)

    assert "CNPJ inválido" in exc_info.value.messages["cnpj"]


def test_schema_rejects_missing_cnpj(schema):
    payload = {}

    with pytest.raises(ValidationError) as exc_info:
        schema.load(payload, partial=("type", "name"))

    assert "CNPJ é obrigatório" in exc_info.value.messages["cnpj"]


def test_schema_rejects_missing_name(schema):
    payload = {"cnpj": "04.252.011/0001-10", "type": "Matriz"}  # Sem o nome

    with pytest.raises(ValidationError) as exc_info:
        schema.load(payload)

    assert "Nome é obrigatório" in exc_info.value.messages["name"]