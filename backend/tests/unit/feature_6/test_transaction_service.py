from unittest.mock import patch, MagicMock
from datetime import date

from app.services.transaction_service import (
    create_transaction,
    update_transaction,
    delete_transaction,
)

DADOS = {
    "description": "Venda de produtos",
    "amount": 150.0,
    "date": date(2025, 5, 1),
    "type": "receita",
    "category_id": 1,
    "company_id": 1,
}


@patch("app.services.transaction_service.Category")
def test_create_transaction_categoria_inexistente(mock_category):
    # Arrange: categoria não existe / não pertence à empresa
    mock_category.query.filter_by.return_value.first.return_value = None

    # Act
    body, status = create_transaction(DADOS, current_user_id=1)

    assert status == 400
    assert "erro" in body


@patch("app.services.transaction_service.db")
@patch("app.services.transaction_service.Transaction")
@patch("app.services.transaction_service.Category")
def test_create_transaction_dados_validos(mock_category, mock_transaction, mock_db):
    mock_category.query.filter_by.return_value.first.return_value = MagicMock()
    mock_transaction.return_value = MagicMock(transaction_id=7)

    # Act
    body, status = create_transaction(DADOS, current_user_id=1)

    assert status == 201
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()


@patch("app.services.transaction_service.Transaction")
def test_update_transaction_inexistente(mock_transaction):
    mock_transaction.query.filter_by.return_value.first.return_value = None

    # Act
    body, status = update_transaction(99, {"description": "novo"}, company_id=1)

    assert status == 404
    assert "erro" in body


@patch("app.services.transaction_service.Transaction")
def test_delete_transaction_inexistente(mock_transaction):
    mock_transaction.query.filter_by.return_value.first.return_value = None

    # Act
    body, status = delete_transaction(99, company_id=1)

    assert status == 404
    assert "erro" in body
