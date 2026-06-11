from app.services.user_service import *
from unittest.mock import patch, MagicMock
import pytest

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
