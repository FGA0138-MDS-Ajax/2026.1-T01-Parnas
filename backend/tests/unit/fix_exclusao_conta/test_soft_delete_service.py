from unittest.mock import patch, MagicMock

from app.models import User
from app.services.user_service import delete_user
from app.services.auth_service import AuthService

@patch('app.services.user_service.db')
def test_delete_user_soft_delete(mock_db):
    mock_user = MagicMock(user_id = 1, is_active = True)
    mock_db.session.query.return_value.filter.return_value.first.return_value = mock_user

    texto, codigo = delete_user(user_id = 1)

    assert codigo == 200
    assert texto["mensagem"] == "Usuário excluído com sucesso."
    assert mock_user.is_active is False
    mock_db.session.delete.assert_not_called()
    mock_db.session.commit.assert_called_once()

@patch('app.services.user_service.db')
def test_delete_user_inexistent(mock_db):
    mock_db.session.query.return_value.filter.return_value.first.return_value = None

    texto, codigo = delete_user(user_id= 999)

    assert codigo == 404
    assert texto["erro"] == "Usuário não encontrado."
    mock_db.session.commit.assert_not_called()
    mock_db.session.delete.assert_not_called()

@patch('app.services.auth_service.find_user_by_email')
def test_login_usuario_inactive(mock_user):
    mock_user.return_value = MagicMock(user_id = 1, is_active = False)

    texto, codigo = AuthService.login("emailteste@gmail.com", "senha@123")

    assert codigo == 401
    assert texto["erro"] == "Conta não encontrada ou desativada"

@patch('app.services.auth_service.find_user_by_email')
def test_login_usuario_inexistent(mock_user):
    mock_user.return_value = None

    texto, codigo = AuthService.login("emailteste@gmail.com", "senha@123")

    assert codigo == 401
    assert texto["erro"] == "Conta não encontrada ou desativada"