import pytest
from marshmallow import ValidationError
from app.schemas.category_schema import CategoryAddSchema


@pytest.fixture
def schema():
    return CategoryAddSchema()


def test_schema_rejects_missing_name(schema):
    payload = {"cnpj": "04.252.011/0001-10", "type": "Matriz"}  # Sem o nome

    with pytest.raises(ValidationError) as exc_info:
        schema.load(payload)

    assert "Nome é obrigatório" in exc_info.value.messages["name"]