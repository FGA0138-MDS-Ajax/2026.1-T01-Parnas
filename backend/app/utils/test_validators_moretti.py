from app.utils.validators import is_valid_password, is_valid_birth_date

def test_is_valid_password_valid():
    assert is_valid_password('Senha@123')

    assert is_valid_password('Senha123')

def test_is_valid_password_empty():
    assert not is_valid_password('')

def test_is_valid_password_short():
    assert not is_valid_password('Abc@1')

def test_is_valid_password_no_special():
    assert not is_valid_password('Abcdefgh123')

def test_is_valid_birth_date_valid():
    assert is_valid_birth_date('2000-05-28')

def test_is_valid_birth_date_invalid():
    assert not is_valid_birth_date('2015-05-28')