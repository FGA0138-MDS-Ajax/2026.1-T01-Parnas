#culpado pelo teste: daniel
# fixtures client, test_user e clean_db do conftest, sem mock
from app.utils.reset_token import generate_reset_token

SENHA_VALIDA = 'Senha@123'
SENHA_NOVA = 'NovaSenha@456'


# --- POST /auth/forgot-password ---

def test_forgot_password_com_email_cadastrado(client, test_user, clean_db):
    resp = client.post('/auth/forgot-password', json={'email': 'teste@email.com'})

    body = resp.get_json()
    assert resp.status_code == 200
    assert body['email'] == 'teste@email.com'
    assert 'reset_link' in body


def test_forgot_password_com_email_nao_cadastrado(client, clean_db):
    resp = client.post('/auth/forgot-password', json={'email': 'fantasma@email.com'})

    assert resp.status_code == 404
    assert resp.get_json() == {"erro": "Usuário não encontrado"}


def test_forgot_password_sem_email(client, clean_db):
    resp = client.post('/auth/forgot-password', json={})

    assert resp.status_code == 400
    assert resp.get_json() == {"erro": "Email obrigatório"}


# --- POST /auth/reset-password (TS-13) ---

def test_redefinir_senha_com_token_valido(client, test_user, clean_db, app_context):
    token = generate_reset_token(test_user.email)

    resp = client.post(
        '/auth/reset-password',
        json={'token': token, 'new_password': SENHA_NOVA},
    )

    assert resp.status_code == 200
    assert resp.get_json() == {"mensagem": "Senha redefinida com sucesso"}


def test_login_funciona_apos_redefinicao(client, test_user, clean_db, app_context):
    token = generate_reset_token(test_user.email)
    client.post(
        '/auth/reset-password',
        json={'token': token, 'new_password': SENHA_NOVA},
    )

    # senha antiga deixa de valer
    login_antigo = client.post(
        '/auth/login', json={'email': test_user.email, 'password': SENHA_VALIDA}
    )
    assert login_antigo.status_code == 401

    # senha nova passa a valer
    login_novo = client.post(
        '/auth/login', json={'email': test_user.email, 'password': SENHA_NOVA}
    )
    assert login_novo.status_code == 200
    assert 'token' in login_novo.get_json()


def test_redefinir_senha_com_token_invalido(client, clean_db):
    resp = client.post(
        '/auth/reset-password',
        json={'token': 'token-falso-e-invalido', 'new_password': SENHA_NOVA},
    )

    assert resp.status_code == 400
    assert resp.get_json() == {"erro": "Token inválido ou expirado"}


def test_redefinir_senha_sem_campos_obrigatorios(client, clean_db):
    resp = client.post('/auth/reset-password', json={'token': 'so-o-token'})

    assert resp.status_code == 400
    assert resp.get_json() == {"erro": "Token e nova senha obrigatórios"}
