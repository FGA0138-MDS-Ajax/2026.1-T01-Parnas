from unittest.mock import patch, MagicMock

from app.services.category_service import (
    add_category,
    get_categories,
    update_category,
    delete_category,
)

DADOS = {"cnpj": "11.222.333/0001-81", "name": "Vendas", "type": "receita"}


@patch("app.services.category_service.Company")
def test_add_category_empresa_inexistente(mock_company):
    mock_company.query.filter_by.return_value.first.return_value = None

    # Act
    body, status = add_category(1, DADOS)

    assert status == 404
    assert "erro" in body


@patch("app.services.category_service.db")
@patch("app.services.category_service.Category")
@patch("app.services.category_service.Company")
def test_add_category_empresa_valida(mock_company, mock_category, mock_db):
    mock_company.query.filter_by.return_value.first.return_value = MagicMock(company_id=10)

    # Act
    body, status = add_category(1, DADOS)

    assert status == 201
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()


@patch("app.services.category_service.Company")
def test_get_categories_empresa_inexistente(mock_company):
    mock_company.query.filter_by.return_value.first.return_value = None

    # Act
    body, status = get_categories(1, {"cnpj": "11.222.333/0001-81"})

    assert status == 404
    assert "erro" in body


@patch("app.services.category_service.Category")
@patch("app.services.category_service.Company")
def test_update_category_inexistente(mock_company, mock_category):
    # Arrange: empresa existe, mas a categoria pedida não pertence a ela
    mock_company.query.filter_by.return_value.first.return_value = MagicMock(company_id=10)
    mock_category.query.filter_by.return_value.first.return_value = None

    # Act
    body, status = update_category(1, {"cnpj": "11.222.333/0001-81", "id": 99, "name": "Novo"})

    assert status == 404
    assert "erro" in body


@patch("app.services.category_service.Category")
@patch("app.services.category_service.Company")
def test_delete_category_inexistente(mock_company, mock_category):
    mock_company.query.filter_by.return_value.first.return_value = MagicMock(company_id=10)
    mock_category.query.filter_by.return_value.first.return_value = None

    # Act
    body, status = delete_category(1, {"cnpj": "11.222.333/0001-81", "id": 99})

    assert status == 404
    assert "erro" in body
