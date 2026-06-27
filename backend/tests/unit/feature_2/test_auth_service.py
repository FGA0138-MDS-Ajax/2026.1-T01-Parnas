from app.services.auth_service import AuthService
from unittest.mock import patch, MagicMock

@patch('app.services.auth_service.find_user_by_email')
def test_login_usuario_inexistente(mock_find):
    mock_find.return_value = None

    body, status = AuthService.login('nao@existe.com', 'Senha@123')

    assert status == 401
    assert body == {"erro": "Conta não encontrada ou desativada"}

@patch('app.services.auth_service.bcrypt')
@patch('app.services.auth_service.find_user_by_email')
def test_login_senha_incorreta(mock_find, mock_bcrypt):
    # Arrange: usuário existe, mas o hash não bate
    mock_find.return_value = MagicMock(password_hash='hash-no-banco')
    mock_bcrypt.checkpw.return_value = False

    body, status = AuthService.login('teste@email.com', 'senha-errada')

    assert status == 401
    assert body == {"erro": "E-mail ou senha inválidos"}

@patch('app.services.auth_service.create_access_token')
@patch('app.services.auth_service.bcrypt')
@patch('app.services.auth_service.find_user_by_email')
def test_login_credenciais_validas(mock_find, mock_bcrypt, mock_token):
    mock_find.return_value = MagicMock(user_id=7, password_hash='hash-no-banco')
    mock_bcrypt.checkpw.return_value = True
    mock_token.return_value = 'jwt-fake'

    body, status = AuthService.login('teste@email.com', 'Senha@123')

    # Assert: 200 com o token e JWT gerado a partir do id do usuário (como string)
    assert status == 200
    assert body == {"token": "jwt-fake"}
    mock_token.assert_called_once_with(identity='7')
