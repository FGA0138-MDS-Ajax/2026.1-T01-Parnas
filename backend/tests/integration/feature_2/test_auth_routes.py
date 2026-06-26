#fixtures client, test_user e clean_db, sem mock

SENHA_VALIDA = 'Senha@123'
def test_login_credenciais_validas(client, test_user, clean_db):
    resp = client.post(
        '/auth/login',
        json={'email': 'teste@email.com', 'password': SENHA_VALIDA},
    )

    assert resp.status_code == 200
    assert 'token' in resp.get_json()

def test_login_senha_incorreta(client, test_user, clean_db):
    resp = client.post(
        '/auth/login',
        json={'email': 'teste@email.com', 'password': 'senha-errada'},
    )

    assert resp.status_code == 401
    assert resp.get_json() == {"erro": "E-mail ou senha inválidos"}

def test_login_email_inexistente(client, clean_db):
    resp = client.post(
        '/auth/login',
        json={'email': 'fantasma@email.com', 'password': SENHA_VALIDA},
    )

    assert resp.status_code == 401
    assert resp.get_json() == {"erro": "Conta não encontrada ou desativada"}

def test_login_sem_campos_obrigatorios(client, clean_db):
    resp = client.post('/auth/login', json={'email': 'teste@email.com'})

    assert resp.status_code == 400
    assert resp.get_json() == {"erro": "E-mail e senha são obrigatórios"}
