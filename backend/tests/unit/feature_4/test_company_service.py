import pytest
from unittest.mock import patch, MagicMock
from app.services.company_service import register_company


@pytest.fixture
def mock_db():
    with patch('app.services.company_service.db') as mock:
        yield mock


@pytest.fixture
def mock_company_model():
    with patch('app.services.company_service.Company') as mock:
        yield mock


def test_register_company_rejects_duplicated_cnpj(mock_company_model):
    mock_company_model.query.filter_by.return_value.first.return_value = MagicMock(cnpj="04252011000110")

    user_id = 1
    data = {
        "name": "Empresa Teste",
        "cnpj": "04.252.011/0001-10",
        "email": "teste@empresa.com",
        "phone": "11999999999"
    }

    response, status_code = register_company(user_id, data)

    assert status_code == 409
    assert response["erro"] == "CNPJ já cadastrado"


@patch('app.services.company_service.user_company')
def test_register_company_binds_user_automatically(mock_user_company, mock_company_model, mock_db):
    mock_company_model.query.filter_by.return_value.first.return_value = None

    fake_new_company = MagicMock()
    fake_new_company.company_id = 99
    fake_new_company.name = "Empresa Nova"
    fake_new_company.cnpj = "04252011000110"

    mock_company_model.return_value = fake_new_company

    user_id = 42
    data = {
        "name": "Empresa Nova",
        "cnpj": "04.252.011/0001-10",
        "email": "nova@empresa.com",
        "phone": "11888888888"
    }

    response, status_code = register_company(user_id, data)

    assert status_code == 201
    assert response["mensagem"] == "Empresa cadastrada com sucesso"
    assert response["company_id"] == 99

    mock_user_company.insert().values.assert_called_once_with(
        user_id=42,
        company_id=99
    )

    assert mock_db.session.add.called
    assert mock_db.session.flush.called
    assert mock_db.session.execute.called
    assert mock_db.session.commit.called