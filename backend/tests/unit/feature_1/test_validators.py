from app.utils.validators import *
import pytest

# - - - - - - - - - - - - - - - - - - - - -
# def is_valid_password(password):

def test_is_valid_password_void():
    # Vazio
    assert is_valid_password(None) is False
    assert is_valid_password('') is False

#Espaços

def test_is_valid_password_too_short():
    # Menos 8 caracteres
    assert is_valid_password('Key67!') is False
def test_is_valid_password_no_special():
    # Sem caracter especial
    assert is_valid_password('Senha677') is False
def test_is_valid_password_no_numbers():
    # Sem número
    assert is_valid_password('Senha!!!') is False
def test_is_valid_password_no_letters():
    # Sem letra
    assert is_valid_password('67!67!67!') is False

@pytest.mark.parametrize("password",[
    'Senha67!',
    '676767S!',
    '!@#$%^&*p3',
])
def test_is_valid_password_valid(password):
    assert is_valid_password(password) is True

# - - - - - - - - - - - - - - - - - - - - -
# def is_valid_birth_date(birth_date_str):

def test_is_valid_birth_date_void():
    # Vazio
    assert is_valid_birth_date(None) is False
    assert is_valid_birth_date('') is False
def test_is_valid_birth_date_future_date():
    # Data futura
    assert is_valid_birth_date('2067-06-07') is False
def test_is_valid_birth_date_minor():
    # Menor de 16
    assert is_valid_birth_date('2026-06-08') is False
    assert is_valid_birth_date('2015-01-01') is False
def test_is_valid_birth_date_invalid_month():
    # Mês inexistente
    assert is_valid_birth_date('2000-13-07') is False
def test_is_valid_birth_date_invalid_day():
    # Dia inexistente
    assert is_valid_birth_date('2000-03-67') is False
def test_is_valid_birth_date_invalid_input():
    # Entrada inválida
    assert is_valid_birth_date('11/09/2001') is False
    assert is_valid_birth_date('2000/01/01') is False
    assert is_valid_birth_date('Mihawk_Upscale') is False

def test_is_valid_birth_date_june_31st():
    # Dia 31 de Junho
    assert is_valid_birth_date('2000-06-31') is False
def test_is_valid_birth_date_february_29th():
    # Dia 29 de Fevereiro
    assert is_valid_birth_date('2015-02-29') is False
    assert is_valid_birth_date('2000-02-29') is True

@pytest.mark.parametrize("date",[
    '2000-01-30',
    '2000-12-01',
    '2001-02-03',
    '2001-09-11',
])
def test_is_valid_birth_date_valid(date):
    assert is_valid_birth_date(date) is True

