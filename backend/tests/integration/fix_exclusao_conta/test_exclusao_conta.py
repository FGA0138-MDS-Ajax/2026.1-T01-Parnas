from encodings import koi8_r

from app.config import db
from app.models.user import User

EMAIL = 'test@email.com'
SENHA = 'senha@123'

def _login(client):
    resultado = client.post('/auth/login', json = {'email': EMAIL, 'password': SENHA})

    assert resultado.status_code == 200, 'pre-condicao: login inicial precisa funcionar'
    return resultado.get_json()['token']

def test_token_excluded_or_blocked_account(client, test_user, clean_db):
    # 1. chama o login e obtem o token
    token = _login(client)
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    # 2. o usuario é deletado
    resultado_delete = client.delete('/api/profile', headers = headers)
    assert resultado_delete.status_code == 200
    assert resultado_delete.get_json()['mensagem'] == 'Usuário excluído com sucesso'
    # 3. usar o token novamente, mas o usuario foi desativado
    resultado_reuso = client.delete('/api/profile' , headers = headers)
    assert resultado_reuso.status_code == 401
    assert resultado_reuso.get_json()['erro'] == 'Conta não encontrada ou desativada'

def test_login_excluded_user(client, test_user, clean_db):
    token = _login(client)
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    assert client.delete('/api/profile', headers = headers) == 200
    resultado_relogin = client.post('/auth/login', json = {'email': EMAIL, 'password': SENHA})
    assert resultado_relogin.status_code == 401
    assert resultado_relogin.get_json()['erro'] == 'Conta não encontrada ou desativada'

def test_preservation_after_soft_delete(client, test_user, clean_db, app_context):
    user_id = test_user.user_id
    token = _login(client)
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    assert client.delete('/api/profile', headers=headers) == 200
    user_db = db.session.query(User).filter(User.user_id == user_id).first()
    assert user_db is not None
    assert user_db.is_active is False