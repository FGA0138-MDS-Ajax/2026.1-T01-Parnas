import pytest
from unittest.mock import patch, MagicMock
from app.services.user_service import delete_user




@patch('app.services.user_service.db')
def test_delete_user_returns_404_if_not_found(mock_db):
    """Garante que o sistema não quebra se tentar deletar um usuário que já não existe"""

    # Simula que a query de busca retornou vazio
    mock_db.session.query.return_value.filter.return_value.first.return_value = None

    response, status_code = delete_user(user_id=99)

    assert status_code == 404
    assert response["erro"] == "Usuário não encontrado."

    # Garante que nada foi deletado
    mock_db.session.delete.assert_not_called()