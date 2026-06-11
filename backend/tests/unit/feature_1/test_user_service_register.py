from app.services.user_service import *
from unittest.mock import patch, MagicMock

# def register_user(data):
# >>essa função retorna uma tupla: dict, int / mensagem, codigo / text, code<<

DATA = {
    'name': 'Daniel',
    'email': 'daniel@gmail.com',
    'cpf': '123.456.789-67',
    'password': 'senha67!',
    'birth_date': '2001-11-09'
}

@patch('app.services.user_service.find_user_by_email')
def test_register_user_email_duplicated(mock_find_user_by_email):
    mock_find_user_by_email.return_value = MagicMock()

    text, code = register_user(DATA)

    assert text == {"erro": "Este e-mail já está cadastrado"}
    assert code == 409


@patch('app.services.user_service.find_user_by_cpf')
@patch('app.services.user_service.find_user_by_email')
def test_register_user_cpf_duplicated(mock_find_user_by_email,mock_find_user_by_cpf):
    mock_find_user_by_email.return_value = None
    mock_find_user_by_cpf.return_value = MagicMock()

    text, code = register_user(DATA)

    assert text == {"erro": "Este CPF já está cadastrado"}
    assert code == 409

@patch('app.services.user_service.create_access_token')
@patch('app.services.user_service.db')
@patch('app.services.user_service.bcrypt')
@patch('app.services.user_service.find_user_by_cpf')
@patch('app.services.user_service.find_user_by_email')
def test_register_user_sucess(mock_find_user_by_email,mock_find_user_by_cpf,mock_bcrypt, mock_db, mock_token):
    mock_find_user_by_email.return_value = None
    mock_find_user_by_cpf.return_value = None
    mock_bcrypt.return_value = b'hashed_password'
    mock_token.return_value = 'fake_token'

    text, code = register_user(DATA)

    assert text['mensagem'] == "Conta criada com sucesso."
    assert text['token'] == 'fake_token'
    assert code == 201
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()

@patch('app.services.user_service.db')
@patch('app.services.user_service.bcrypt')
@patch('app.services.user_service.find_user_by_cpf')
@patch('app.services.user_service.find_user_by_email')
def test_register_user_internal_error(mock_find_user_by_email,mock_find_user_by_cpf,mock_bcrypt, mock_db):
    mock_find_user_by_email.return_value = None
    mock_find_user_by_cpf.return_value = None
    mock_bcrypt.hashpw.return_value = b'hashed'
    mock_db.session.commit.side_effect = Exception('erro no banco')

    response, status = register_user(DATA)

    assert status == 500
    assert response['erro'] == 'Ocorreu um erro interno ao tentar salvar o usuário.'
    mock_db.session.rollback.assert_called_once()