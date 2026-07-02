# daniel: ajustei as assinaturas - create_transaction(data, user_id),
# update_transaction(transaction_id, user_id, data), delete_transaction(transaction_id, user_id);
# e mocko _validate_user_company_access, que o create passou a checar antes da categoria.
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






@patch("app.services.transaction_service.Transaction")
def test_update_transaction_inexistente(mock_transaction):
    mock_transaction.query.filter_by.return_value.first.return_value = None

    # Act
    body, status = update_transaction(99, 1, {"description": "novo"})

    assert status == 404
    assert "erro" in body


@patch("app.services.transaction_service.Transaction")
def test_delete_transaction_inexistente(mock_transaction):
    mock_transaction.query.filter_by.return_value.first.return_value = None

    # Act
    body, status = delete_transaction(99, 1)

    assert status == 404
    assert "erro" in body
