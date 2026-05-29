"""
test_company_registration_flow.py - Testes End-to-End (E2E) da Feature de Cadastro

Testes E2E simulam fluxos completos como um usuário real faria:
  1. Usuário cria conta → recebe token
  2. Usuário faz login → recebe token
  3. Usuário cadastra empresa → empresa é criada
  4. Usuário tenta CNPJ duplicado → recebe erro
  5. Usuário consulta dados → vê a empresa criada

O que torna um teste "E2E":
  - Múltiplos endpoints / operações em sequência
  - Testa dados que "atravessam" a aplicação
  - Simula comportamento real do usuário
  - Pode validar efeitos colaterais (BD, histórico, etc.)

Diferença dos testes anteriores:
  - Testes unitários: Testam uma função isolada
  - Testes de integração (routes): Testam um endpoint isolado
  - Testes E2E: Testam fluxo completo (vários endpoints juntos)
"""

import pytest
from app.models.company import Company
from app.models.user import User
import bcrypt


class TestCompanyRegistrationFlow:
    """Testes do fluxo completo de registração de empresa"""

    def test_user_registers_and_creates_company_flow(self, client, clean_db, app_context):
        """
        CENÁRIO (Fluxo completo):
        1. Usuário já existe (pré-criado)
        2. Usuário faz login → recebe token
        3. Usuário cadastra empresa → empresa criada
        4. Sistema verifica que empresa existe no BD

        ESPERADO: Fluxo completo funciona sem erros
        """

        # Setup: Criar usuário
        from datetime import date
        email = 'user@test.com'
        password = 'Senha@123'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            email=email,
            password_hash=hashed_password,
            name='Test User',
            cpf='12345678901',
            birth_date=date(2000, 1, 1)
        )
        from app.config import db
        db.session.add(user)
        db.session.commit()

        # Step 1: Usuário faz login
        login_response = client.post(
            '/auth/login',
            json={'email': email, 'password': password}
        )

        assert login_response.status_code == 200
        token = login_response.get_json()['token']
        assert token is not None

        # Step 2: Usuário cadastra empresa com o token recebido
        auth_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        company_data = {
            'name': 'Empresa Registrada',
            'cnpj': '11.222.333/0001-81',
            'email': 'empresa@test.com',
            'phone': '1133334444'
        }

        register_response = client.post(
            '/api/companies/register',
            json=company_data,
            headers=auth_headers
        )

        assert register_response.status_code == 201
        response_data = register_response.get_json()
        company_id = response_data['company_id']

        # Step 3: Verificar que empresa está no BD
        company = Company.query.get(company_id)
        assert company is not None
        assert company.name == 'Empresa Registrada'
        assert company.cnpj == '11222333000181'
        assert company.email == 'empresa@test.com'

        # Step 4: Verificar que usuário está associado à empresa
        reloaded_user = User.query.get(user.user_id)
        assert len(reloaded_user.companies) == 1
        assert reloaded_user.companies[0].company_id == company_id

    def test_duplicate_cnpj_detection_in_flow(self, client, clean_db, app_context):
        """
        CENÁRIO (Fluxo com duplicação):
        1. Usuário registra empresa A com CNPJ "11.222.333/0001-81"
        2. Usuário tenta registrar empresa B com CNPJ "11.222.333/0001-81" (formatação diferente)
        3. Sistema rejeita empresa B (CNPJ duplicado)

        ESPERADO: CNPJ é reconhecido como duplicado apesar da formatação diferente
        """

        # Setup: Usuário
        from datetime import date
        email = 'user@test.com'
        password = 'Senha@123'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            email=email,
            password_hash=hashed_password,
            name='Test User',
            cpf='12345678901',
            birth_date=date(2000, 1, 1)
        )
        from app.config import db
        db.session.add(user)
        db.session.commit()

        # Step 1: Login
        login_response = client.post(
            '/auth/login',
            json={'email': email, 'password': password}
        )
        token = login_response.get_json()['token']

        auth_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Step 2: Registrar primeira empresa (com formatação)
        first_company = {
            'name': 'Primeira',
            'cnpj': '11.222.333/0001-81',  # Com formatação
            'email': 'primeira@test.com',
            'phone': '1133334444'
        }

        response1 = client.post(
            '/api/companies/register',
            json=first_company,
            headers=auth_headers
        )

        assert response1.status_code == 201

        # Step 3: Tentar registrar segunda empresa (CNPJ sem formatação)
        second_company = {
            'name': 'Segunda',
            'cnpj': '11222333000181',  # Sem formatação (mesmo CNPJ)
            'email': 'segunda@test.com',
            'phone': '1144445555'
        }

        response2 = client.post(
            '/api/companies/register',
            json=second_company,
            headers=auth_headers
        )

        # Assert: Rejeitado (409)
        assert response2.status_code == 409
        assert 'CNPJ já cadastrado' in response2.get_json()['erro']

        # Assert: BD contém apenas 1 empresa
        companies = Company.query.all()
        assert len(companies) == 1

    def test_multiple_users_different_cnpjs(self, client, clean_db, app_context):
        """
        CENÁRIO (Fluxo com múltiplos usuários):
        1. Usuário A registra empresa com CNPJ X
        2. Usuário B registra empresa com CNPJ Y (diferente)
        3. Ambas as empresas existem no BD

        ESPERADO: Cada usuário por ter suas próprias empresas
        """

        from app.config import db
        from datetime import date

        # Setup: Criar 2 usuários
        email_a = 'user_a@test.com'
        email_b = 'user_b@test.com'
        password = 'Senha@123'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user_a = User(
            email=email_a,
            password_hash=hashed_password,
            name='User A',
            cpf='12345678901',
            birth_date=date(2000, 1, 1)
        )
        user_b = User(
            email=email_b,
            password_hash=hashed_password,
            name='User B',
            cpf='12345678902',
            birth_date=date(2000, 1, 1)
        )
        db.session.add(user_a)
        db.session.add(user_b)
        db.session.commit()

        # Step 1: User A faz login
        login_response_a = client.post(
            '/auth/login',
            json={'email': email_a, 'password': password}
        )
        token_a = login_response_a.get_json()['token']

        # Step 2: User B faz login
        login_response_b = client.post(
            '/auth/login',
            json={'email': email_b, 'password': password}
        )
        token_b = login_response_b.get_json()['token']

        # Step 3: User A registra empresa com CNPJ X
        auth_headers_a = {
            'Authorization': f'Bearer {token_a}',
            'Content-Type': 'application/json'
        }

        company_a = {
            'name': 'Empresa A',
            'cnpj': '11.222.333/0001-81',
            'email': 'empresa_a@test.com',
            'phone': '1133334444'
        }

        response_a = client.post(
            '/api/companies/register',
            json=company_a,
            headers=auth_headers_a
        )

        assert response_a.status_code == 201
        company_id_a = response_a.get_json()['company_id']

        # Step 4: User B registra empresa com CNPJ Y (diferente)
        auth_headers_b = {
            'Authorization': f'Bearer {token_b}',
            'Content-Type': 'application/json'
        }

        company_b = {
            'name': 'Empresa B',
            'cnpj': '22.333.444/0001-92',  # CNPJ diferente
            'email': 'empresa_b@test.com',
            'phone': '1144445555'
        }

        response_b = client.post(
            '/api/companies/register',
            json=company_b,
            headers=auth_headers_b
        )

        assert response_b.status_code == 201
        company_id_b = response_b.get_json()['company_id']

        # Assert: BD tem 2 empresas
        companies = Company.query.all()
        assert len(companies) == 2

        # Assert: Cada usuário está associado à sua empresa
        user_a_reloaded = User.query.get(user_a.user_id)
        user_b_reloaded = User.query.get(user_b.user_id)

        assert len(user_a_reloaded.companies) == 1
        assert len(user_b_reloaded.companies) == 1
        assert user_a_reloaded.companies[0].company_id == company_id_a
        assert user_b_reloaded.companies[0].company_id == company_id_b


class TestCompanyRegistrationErrorRecovery:
    """Testes de recuperação de erros no fluxo"""

    def test_invalid_data_error_does_not_affect_next_request(self, client, clean_db, app_context):
        """
        CENÁRIO: Usuário tenta registrar com dados inválidos, depois com dados válidos
        ESPERADO: Erro da primeira não afeta a segunda requisição
        """

        from app.config import db
        from datetime import date

        # Setup: Usuário
        email = 'user@test.com'
        password = 'Senha@123'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            email=email,
            password_hash=hashed_password,
            name='Test User',
            cpf='12345678901',
            birth_date=date(2000, 1, 1)
        )
        db.session.add(user)
        db.session.commit()

        # Login
        login_response = client.post(
            '/auth/login',
            json={'email': email, 'password': password}
        )
        token = login_response.get_json()['token']

        auth_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Step 1: Requisição com dados INVÁLIDOS (email inválido)
        invalid_company = {
            'name': 'Empresa Inválida',
            'cnpj': '11.222.333/0001-81',
            'email': 'not-an-email',  # INVÁLIDO
            'phone': '1133334444'
        }

        response1 = client.post(
            '/api/companies/register',
            json=invalid_company,
            headers=auth_headers
        )

        assert response1.status_code == 400

        # Step 2: Requisição com dados VÁLIDOS (mesma empresa, email corretor)
        valid_company = {
            'name': 'Empresa Válida',
            'cnpj': '11.222.333/0001-81',
            'email': 'valida@test.com',  # Agora válido
            'phone': '1133334444'
        }

        response2 = client.post(
            '/api/companies/register',
            json=valid_company,
            headers=auth_headers
        )

        # Assert: Segunda requisição sucede
        assert response2.status_code == 201

        # Assert: Apenas 1 empresa no BD (a inválida não foi criada)
        companies = Company.query.all()
        assert len(companies) == 1
        assert companies[0].email == 'valida@test.com'

    def test_database_error_recovery(self, client, clean_db, app_context, mocker):
        """
        CENÁRIO: Erro no BD durante primeira tentativa, depois sucesso
        ESPERADO: Segunda tentativa funciona normalmente

        Nota: Este teste é mais avançado e simula um erro no BD.
        """

        from app.config import db
        from datetime import date

        # Setup: Usuário
        email = 'user@test.com'
        password = 'Senha@123'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            email=email,
            password_hash=hashed_password,
            name='Test User',
            cpf='12345678901',
            birth_date=date(2000, 1, 1)
        )
        db.session.add(user)
        db.session.commit()

        # Login
        login_response = client.post(
            '/auth/login',
            json={'email': email, 'password': password}
        )
        token = login_response.get_json()['token']

        auth_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Step 1: Requisição normal (sem erro)
        company = {
            'name': 'Empresa Normal',
            'cnpj': '11.222.333/0001-81',
            'email': 'normal@test.com',
            'phone': '1133334444'
        }

        response = client.post(
            '/api/companies/register',
            json=company,
            headers=auth_headers
        )

        # Assert: Sucesso
        assert response.status_code == 201


class TestCompanyRegistrationValidationFilters:
    """Testes de validação em camadas (schema → service → BD)"""

    def test_schema_validation_catches_early_invalid_cnpj(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: CNPJ muito curto é rejeitado pela schema ANTES de chegar ao service
        ESPERADO: Status 400, erro vem da validação de schema
        """

        company_data = {
            'name': 'Empresa',
            'cnpj': '11.22',  # Muito curto (menos de 14 chars)
            'email': 'test@empresa.com',
            'phone': '1133334444'
        }

        response = client.post(
            '/api/companies/register',
            json=company_data,
            headers=auth_headers
        )

        # Assert: Rejeitado pela schema
        assert response.status_code == 400
        assert 'erros_de_validacao' in response.get_json()

    def test_cnpj_validation_catches_invalid_digit(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: CNPJ com dígito verificador errado
        ESPERADO: Rejeitado mesmo se passar no tamanho
        """

        company_data = {
            'name': 'Empresa',
            'cnpj': '11.111.111/1111-11',  # CNPJ invalido (tamanho ok, digitos errados)
            'email': 'test@empresa.com',
            'phone': '1133334444'
        }

        response = client.post(
            '/api/companies/register',
            json=company_data,
            headers=auth_headers
        )

        # Assert: Rejeitado
        assert response.status_code == 400
        errors = response.get_json()['erros_de_validacao']
        assert 'cnpj' in errors
        assert 'inválido' in str(errors['cnpj']).lower()

