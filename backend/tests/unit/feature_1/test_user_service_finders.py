from app.services.user_service import *
from unittest.mock import patch, MagicMock

# def find_user_by_email(email: str):
# >>essa função retorna um User (ou None)<<

@patch('app.services.user_service.db')
def test_find_user_by_email_found(mock_db):
    mock_user = MagicMock()

    mock_db.session.query.return_value.filter.return_value.first.return_value = mock_user
    result = find_user_by_email('daniel@gmail.com')

    assert result == mock_user

@patch('app.services.user_service.db')
def test_find_user_by_email_not_found(mock_db):
    mock_db.session.query.return_value.filter.return_value.first.return_value = None
    result = find_user_by_email('daniel@gmail.com')

    assert result is None
    mock_db.session.query.assert_called_once()

@patch('app.services.user_service.db')
def test_find_user_by_email_void(mock_db):
    result = find_user_by_email('')

    assert result is None
    mock_db.session.query.assert_not_called()

# def find_user_by_cpf(cpf: str):
# >>essa função retorna um User (ou None)<<

@patch('app.services.user_service.db')
def test_find_user_by_cpf_found(mock_db):
    mock_user = MagicMock()

    mock_db.session.query.return_value.filter.return_value.first.return_value = mock_user
    result = find_user_by_cpf('123.456.789-67')

    assert result == mock_user

@patch('app.services.user_service.db')
def test_find_user_by_cpf_not_found(mock_db):
    mock_db.session.query.return_value.filter.return_value.first.return_value = None
    result = find_user_by_cpf('123.456.789-67')

    assert result is None
    mock_db.session.query.assert_called_once()

@patch('app.services.user_service.db')
def test_find_user_by_cpf_void(mock_db):
    result = find_user_by_cpf('')

    assert result is None
    mock_db.session.query.assert_not_called()
