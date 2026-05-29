#rascunho ainda
from app.services.auth_service import AuthService
def test_login_valido():
    assert AuthService().login("joao@gmail.com", "cudecurioso")

def test_login_invalido():
    assert not AuthService().login("2222222222", "EITAPOHA")