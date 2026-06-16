import pytest
from marshmallow import ValidationError
from app.schemas.category_schema import CategoryAddSchema


@pytest.fixture
def schema():
    """Fixture do pytest para instanciar o schema apenas uma vez"""
    return CategoryAddSchema()


def test_schema_accepts_known_valid_cnpj(schema):
    # Passamos partial=True para o Marshmallow ignorar a obrigatoriedade
    # dos campos 'name' e 'type', focando apenas no 'cnpj'
    payload = {"cnpj": "04.252.011/0001-10"}

    # Se o CNPJ for válido, o load() não lança exceção e retorna o dicionário
    result = schema.load(payload, partial=True)

    assert result["cnpj"] == "04.252.011/0001-10"


def test_schema_rejects_cnpj_with_wrong_length(schema):
    payload = {"cnpj": "123"}

    # Usamos o pytest.raises para capturar o erro de validação
    with pytest.raises(ValidationError) as exc_info:
        schema.load(payload, partial=True)

    # Verifica se a mensagem de erro específica está no campo 'cnpj'
    assert "CNPJ inválido" in exc_info.value.messages["cnpj"]


def test_schema_rejects_cnpj_with_invalid_check_digits(schema):
    payload = {"cnpj": "11.111.111/1111-11"}

    with pytest.raises(ValidationError) as exc_info:
        schema.load(payload, partial=True)

    assert "CNPJ inválido" in exc_info.value.messages["cnpj"]


def test_schema_rejects_missing_cnpj(schema):
    # Teste adicional recomendado: garante que o erro de campo obrigatório funciona
    payload = {}

    with pytest.raises(ValidationError) as exc_info:
        # Aqui ignoramos 'type' e 'name', mas exigimos o resto
        schema.load(payload, partial=("type", "name"))

    assert "CNPJ é obrigatório" in exc_info.value.messages["cnpj"]