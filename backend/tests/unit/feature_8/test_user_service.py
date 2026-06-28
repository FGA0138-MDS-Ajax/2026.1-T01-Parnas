import pytest
from unittest.mock import patch, MagicMock
from app.services.user_service import delete_user


@patch('app.services.user_service.db')
def test_delete_user_success(mock_db):
    """Cobre o Critério: Usuário consegue excluir sua própria conta"""

    # 1. Simula que o usuário existe no banco de dados
    mock_user = MagicMock(user_id=1, email="usuario@teste.com", is_active = True)
    mock_db.session.query.return_value.filter.return_value.first.return_value = mock_user

    # 2. Chama a função de exclusão
    response, status_code = delete_user(user_id=1)

    # 3. Verifica a resposta de sucesso
    assert status_code == 200
    assert response["mensagem"] == "Usuário excluído com sucesso."

    # 4. por conta do soft delete não apaga direto do banco
    mock_db.session.delete.assert_not_called(mock_user)
    assert mock_user.is_active() is False
    mock_db.session.commit.assert_called_once()


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