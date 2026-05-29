"""
conftest.py - Fixtures compartilhadas para todos os testes

Este arquivo contém configurações e fixtures que são usado em múltiplos arquivos de teste.
Pytest carrega automaticamente fixtures do conftest.py.

Fixtures aqui:
- app: Aplicação Flask configurada para testes
- client: Cliente HTTP para fazer requisições de teste
- app_context: Contexto da aplicação
- db_session: Sessão do banco de dados para testes
- clean_db: Limpa o BD antes de cada teste
- auth_token: Token JWT válido para usuário autenticado
"""

import pytest
import os
from app import create_app
from app.config import db, Config
from app.models.user import User
from app.models.company import Company
from flask_jwt_extended import create_access_token
import bcrypt


class TestConfig(Config):
    """Configuração especial para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # BD em memória para testes
    JWT_SECRET_KEY = 'test-key-super-secreto'


@pytest.fixture(scope='session')
def app():
    """
    Cria aplicação Flask para testes (escopo de sessão).
    Escopo 'session' significa que a app é criada uma única vez para toda a sessão de testes.
    """
    application = create_app()
    application.config.from_object(TestConfig)

    # Cria contexto da aplicação para testes
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Cliente HTTP do Flask para fazer requisições de teste.
    Escopo de função = criado novo para cada teste
    """
    return app.test_client()


@pytest.fixture
def app_context(app):
    """
    Contexto da aplicação Flask.
    Necessário para qualquer operação com banco de dados fora de requisições HTTP.
    """
    with app.app_context():
        yield app


@pytest.fixture
def clean_db(app):
    """
    Limpa o banco de dados antes de cada teste.
    Remove todos os registros de todas as tabelas.
    """
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield
        # Teardown: limpar após o teste
        db.session.remove()
        db.drop_all()
        db.create_all()


@pytest.fixture
def test_user(app_context, clean_db):
    """
    Cria um usuário de teste e o persiste no BD.
    
    Returns:
        User: Usuário criado com:
            - email: 'teste@email.com'
            - user_id: Gerado automaticamente
    """
    from datetime import date
    hashed_password = bcrypt.hashpw('Senha@123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user = User(
        email='teste@email.com',
        password_hash=hashed_password,
        name='Usuário Teste',
        cpf='12345678901',
        birth_date=date(2000, 1, 1)
    )
    db.session.add(user)
    db.session.commit()
    
    return user


@pytest.fixture
def auth_token(test_user, app):
    """
    Gera um token JWT válido para o usuário de teste.

    Returns:
        str: Token JWT válido para autenticação
    """
    with app.app_context():
        token = create_access_token(identity=str(test_user.user_id))
    return token


@pytest.fixture
def auth_headers(auth_token):
    """
    Headers HTTP com autenticação JWT.
    Use em requisições que precisam de autenticação.

    Returns:
        dict: Headers com 'Authorization: Bearer {token}'
    """
    return {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }


# ==================== EXEMPLO DE USO ====================
#
# # Teste simples usando fixtures
# def test_exemplo(client, auth_headers, clean_db):
#     """
#     Exemplo de como usar as fixtures.
#     - client: cliente HTTP
#     - auth_headers: headers com token JWT
#     - clean_db: BD limpo antes do teste
#     """
#     response = client.post(
#         '/api/companies/register',
#         json={
#             'name': 'Empresa Teste',
#             'cnpj': '11.222.333/0001-81',
#             'email': 'empresa@email.com',
#             'phone': '1133334444'
#         },
#         headers=auth_headers
#     )
#     assert response.status_code == 201

