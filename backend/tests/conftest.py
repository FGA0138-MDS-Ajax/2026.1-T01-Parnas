"""
conftest.py - Fixtures compartilhadas por TODOS os testes do backend.

O pytest carrega este arquivo automaticamente. Tudo que estiver aqui fica
disponível como fixture em qualquer teste de tests/unit, tests/integration e
tests/e2e — sem precisar importar.

Fixtures disponíveis:
- app           : aplicação Flask configurada para testes (SQLite em memória)
- client        : cliente HTTP do Flask para chamar endpoints
- app_context   : contexto de app para operar o BD fora de uma requisição HTTP
- clean_db      : zera o banco antes e depois de cada teste
- test_user     : um usuário já persistido no banco
- auth_token    : JWT válido do test_user
- auth_headers  : headers HTTP com o JWT (use em requisições autenticadas)
"""

import pytest
from datetime import date

from app import create_app
from app.config import db, Config
from app.models.user import User
from flask_jwt_extended import create_access_token
import bcrypt


class TestConfig(Config):
    """Configuração usada só em testes: banco em memória, rápido e descartável."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-key-super-secreto'


@pytest.fixture(scope='session')
def app():
    """App Flask criada uma vez por sessão de testes."""
    application = create_app()
    application.config.from_object(TestConfig)

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente HTTP do Flask (novo a cada teste)."""
    return app.test_client()


@pytest.fixture
def app_context(app):
    """Contexto de aplicação para mexer no BD fora de uma requisição HTTP."""
    with app.app_context():
        yield app


@pytest.fixture
def clean_db(app):
    """Garante um banco limpo antes e depois do teste."""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()
        db.create_all()


@pytest.fixture
def test_user(app_context, clean_db):
    """Cria e persiste um usuário de teste (email: teste@email.com)."""
    hashed = bcrypt.hashpw('Senha@123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(
        email='teste@email.com',
        password_hash=hashed,
        name='Usuário Teste',
        cpf='12345678901',
        birth_date=date(2000, 1, 1),
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_token(test_user, app):
    """JWT válido para o test_user."""
    with app.app_context():
        return create_access_token(identity=str(test_user.user_id))


@pytest.fixture
def auth_headers(auth_token):
    """Headers HTTP com Bearer token. Use em requisições que exigem login."""
    return {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

@pytest.fixture
def valid_company_payload():
     return {
		"name": "Empresa de Teste LTDA",
		"cnpj": "04.252.011/0001-10",
		"email": "empresa@teste.com",
		"phone": "11999999999",
	}


@pytest.fixture
def payload_without_name(valid_company_payload):
    payload = valid_company_payload.copy()
    payload.pop("name")
    return payload


@pytest.fixture
def payload_without_cnpj(valid_company_payload):
    payload = valid_company_payload.copy()
    payload.pop("cnpj")
    return payload


@pytest.fixture
def payload_with_invalid_cnpj(valid_company_payload):
    payload = valid_company_payload.copy()
    payload["cnpj"] = "11.111.111/1111-11"
    return payload

