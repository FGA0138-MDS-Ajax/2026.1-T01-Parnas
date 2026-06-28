#culpado pelo teste: matheus
import pytest
from flask import Flask
from app.utils.reset_token import generate_reset_token, verify_reset_token


@pytest.fixture
def app_context():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chave-super-secreta-de-teste-67'
    with app.app_context():
        yield app


def test_generate_and_verify_reset_token_success(app_context):
    email = "usuario@teste.com"

    token = generate_reset_token(email)
    assert token is not None

    #happy path
    email_recuperado = verify_reset_token(token)
    assert email_recuperado == email


def test_verify_reset_token_expires_correctly(app_context):
    email = "usuario@teste.com"
    token = generate_reset_token(email)

    email_recuperado = verify_reset_token(token, expiration=-1)

    assert email_recuperado is None


def test_verify_reset_token_rejects_invalid_token(app_context):
    email_recuperado = verify_reset_token("token-completamente-invalido-e-falso")
    assert email_recuperado is None
