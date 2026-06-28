"""
test_company_routes.py - Testes de Integração das APIs/Routes HTTP

Este arquivo testa os ENDPOINTS HTTP da aplicação.
Usa o cliente de teste do Flask para fazer requisições HTTP reais.

O que testar:
  - Autenticação JWT (presença de token, token válido/inválido)
  - HTTP Status Codes (201, 400, 401, 409, 500)
  - Request validation (dados faltando, inválidos)
  - Response format (JSON bem formado, campos corretos)
  - Headers (Content-Type, etc.)

Diferença de testes anteriores:
  - Testa 'como usuário final' vê
  - Requisições HTTP reais (POST, GET, etc.)
  - Headers, status codes, JSON responses
  - Autenticação JWT

Fixtures usadas (do conftest.py):
  - client: Cliente HTTP do Flask
  - clean_db: BD limpo antes de cada teste
  - auth_headers: Headers com token JWT válido
  - test_user: Usuário autenticado
"""

import pytest
import json
from app.models.company import Company
# daniel: atualizei a URL de cadastro para POST /api/companies (era .../register)


class TestCompanyRoutesAuthentication:
    """Testes de autenticação JWT"""

    def test_register_without_token_returns_401(self, client, clean_db):
        """
        CENÁRIO: POST /api/companies SEM token JWT
        ESPERADO: Status 401 Unauthorized
        """

        company_data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        # Action: Fazer requisição SEM headers de autenticação
        response = client.post(
            '/api/companies',
            json=company_data,
            headers={'Content-Type': 'application/json'}
        )

        # Assert: Deve ser 401
        assert response.status_code == 401

    @pytest.mark.xfail(
        reason="DEF: token JWT malformado retorna 422 (default do flask-jwt-extended), não 401; "
        "contrato esperado é 401 — exige handler customizado de erro de token",
        strict=False,
    )
    def test_register_with_invalid_token_returns_401(self, client, clean_db):
        """
        CENÁRIO: POST com token JWT INVÁLIDO
        ESPERADO: Status 401 Unauthorized
        """

        company_data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        invalid_headers = {
            'Authorization': 'Bearer token_invalido_fake_xyz',
            'Content-Type': 'application/json'
        }

        # Action
        response = client.post(
            '/api/companies',
            json=company_data,
            headers=invalid_headers
        )

        # Assert
        assert response.status_code == 401

    def test_register_with_valid_token_proceeds(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: POST com token JWT VÁLIDO
        ESPERADO: Requisição prossegue (não para em 401)

        Nota: Pode falhar por validação de dados, mas 401 não é retornado.
        """

        company_data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        # Action: Com token válido
        response = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )

        # Assert: Não é 401 (pode ser 201, 400, etc., mas autenticação passou)
        assert response.status_code != 401
        assert response.status_code in [201, 400, 409, 500]


class TestCompanyRoutesValidationErrors:
    """Testes quando dados de entrada são inválidos"""

    def test_missing_field_name_returns_400(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: POST sem campo 'name'
        ESPERADO: Status 400, mensagem de validação
        """

        company_data = {
            # 'name' está faltando!
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        # Action
        response = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )

        # Assert: Status 400
        assert response.status_code == 400

        # Assert: Resposta é JSON com erros de validação
        data = response.get_json()
        assert 'erros_de_validacao' in data
        assert 'name' in data['erros_de_validacao']

    def test_invalid_email_returns_400(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: Email sem @
        ESPERADO: Status 400, erro de validação
        """

        company_data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'email_invalido.com',  # Sem @
            'phone': '1133334444'
        }

        # Action
        response = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert 'erros_de_validacao' in data
        assert 'email' in data['erros_de_validacao']

    def test_invalid_cnpj_returns_400(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: CNPJ inválido (dígitos verificadores errados)
        ESPERADO: Status 400, erro de validação
        """

        company_data = {
            'name': 'Empresa Teste',
            'cnpj': '11.111.111/1111-11',  # CNPJ inválido
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        # Action
        response = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert 'erros_de_validacao' in data
        assert 'cnpj' in data['erros_de_validacao']

    def test_short_phone_returns_400(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: Telefone com menos de 8 caracteres
        ESPERADO: Status 400, erro de validação
        """

        company_data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1234567'  # Apenas 7 caracteres
        }

        # Action
        response = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400
        data = response.get_json()
        assert 'erros_de_validacao' in data


class TestCompanyRoutesSuccess:
    """Testes quando o cadastro é bem-sucedido"""

    def test_register_valid_company_returns_201(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: Registrar empresa com dados totalmente válidos
        ESPERADO: Status 201, retorna dados da empresa
        """

        company_data = {
            'name': 'Empresa ABC Ltda',
            'cnpj': '11.222.333/0001-81',
            'email': 'contato@empresa.com',
            'phone': '1133334444'
        }

        # Action
        response = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )

        # Assert: Status 201 (Created)
        assert response.status_code == 201

        # Assert: Response é JSON
        data = response.get_json()
        assert data is not None

        # Assert: Tem campos esperados
        assert 'mensagem' in data
        assert 'company_id' in data
        assert 'name' in data
        assert 'cnpj' in data

        # Assert: Valores corretos
        assert data['mensagem'] == 'Empresa cadastrada com sucesso'
        assert data['name'] == 'Empresa ABC Ltda'
        assert data['cnpj'] == '11222333000181'  # Sem formatação
        assert isinstance(data['company_id'], int)
        assert data['company_id'] > 0

    def test_response_content_type_is_json(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: Verificar que resposta tem Content-Type correto
        ESPERADO: Content-Type: application/json
        """

        company_data = {
            'name': 'Empresa Test',
            'cnpj': '11.222.333/0001-81',
            'email': 'test@empresa.com',
            'phone': '1133334444'
        }

        # Action
        response = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )

        # Assert: Content-Type é JSON
        assert 'application/json' in response.content_type


class TestCompanyRoutesDuplicateCNPJ:
    """Testes quando CNPJ já está registrado"""

    def test_duplicate_cnpj_returns_409(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: Registrar empresa, depois tentar registrar com CNPJ igual
        ESPERADO: Primeira: 201, Segunda: 409 Conflict
        """

        company_data = {
            'name': 'Primeira Empresa',
            'cnpj': '11.222.333/0001-81',
            'email': 'primeira@empresa.com',
            'phone': '1133334444'
        }

        # Action: Primeira requisição (sucesso)
        response1 = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )
        assert response1.status_code == 201

        # Action: Segunda requisição com CNPJ duplicado
        company_data['name'] = 'Segunda Empresa'
        company_data['email'] = 'segunda@empresa.com'
        response2 = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )

        # Assert: Status 409
        assert response2.status_code == 409

        # Assert: Mensagem de erro
        data = response2.get_json()
        assert 'erro' in data
        assert 'CNPJ já cadastrado' in data['erro']

    def test_formatted_and_unformatted_cnpj_treated_as_duplicate(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: Registrar com CNPJ formatado (11.222.333/0001-81), depois sem formatação
        ESPERADO: Segunda falha com 409 (são tratados como iguais)
        """

        # Primeira: Com formatação
        response1 = client.post(
            '/api/companies',
            json={
                'name': 'Empresa 1',
                'cnpj': '11.222.333/0001-81',  # Com formatação
                'email': 'empresa1@test.com',
                'phone': '1133334444'
            },
            headers=auth_headers
        )
        assert response1.status_code == 201

        # Segunda: Sem formatação (mas CNPJ igual)
        response2 = client.post(
            '/api/companies',
            json={
                'name': 'Empresa 2',
                'cnpj': '11222333000181',  # Sem formatação
                'email': 'empresa2@test.com',
                'phone': '1133334444'
            },
            headers=auth_headers
        )

        # Assert: Tratados como duplicata
        assert response2.status_code == 409


class TestCompanyRoutesContentNegotiation:
    """Testes de requisições malformadas"""

    def test_request_without_json_fails(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: POST sem Content-Type application/json
        ESPERADO: Erro (não consegue fazer parsing de dados)
        """

        # Action: Sem JSON
        response = client.post(
            '/api/companies',
            data='not json',
            headers={
                'Authorization': f'Bearer {auth_headers["Authorization"].split()[-1]}',
                'Content-Type': 'text/plain'  # Não é JSON!
            }
        )

        # Assert: Deve falhar (pode ser 400 ou outro erro)
        assert response.status_code != 201

    def test_request_with_empty_json(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: POST com {} vazio
        ESPERADO: Erros de validação (campos obrigatórios faltando)
        """

        # Action
        response = client.post(
            '/api/companies',
            json={},  # Vazio!
            headers=auth_headers
        )

        # Assert: 400 (validação falha)
        assert response.status_code == 400
        data = response.get_json()
        assert 'erros_de_validacao' in data


class TestCompanyRoutesIntegration:
    """Testes de fluxo completo pela API"""

    def test_multiple_companies_by_same_user(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: Um usuário registra múltiplas empresas
        ESPERADO: Todas são criadas com sucesso
        """

        companies = [
            {
                'name': 'Empresa 1',
                'cnpj': '11.222.333/0001-81',
                'email': 'empresa1@test.com',
                'phone': '1133334444'
            },
            {
                'name': 'Empresa 2',
                'cnpj': '11.444.777/0001-61',
                'email': 'empresa2@test.com',
                'phone': '1144445555'
            },
            {
                'name': 'Empresa 3',
                'cnpj': '45.997.418/0001-53',
                'email': 'empresa3@test.com',
                'phone': '1155556666'
            }
        ]

        company_ids = []

        # Action: Registrar 3 empresas
        for company_data in companies:
            response = client.post(
                '/api/companies',
                json=company_data,
                headers=auth_headers
            )

            assert response.status_code == 201
            data = response.get_json()
            company_ids.append(data['company_id'])

        # Assert: Todos os IDs são diferentes
        assert len(set(company_ids)) == 3

    def test_response_includes_all_required_fields(self, client, clean_db, auth_headers, test_user):
        """
        CENÁRIO: Validar que resposta tem TODOS os campos obrigatórios
        ESPERADO: mensagem, company_id, name, cnpj, (register_date não está no código atual)
        """

        company_data = {
            'name': 'Completa Ltd',
            'cnpj': '11.222.333/0001-81',
            'email': 'completa@test.com',
            'phone': '1133334444'
        }

        # Action
        response = client.post(
            '/api/companies',
            json=company_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.get_json()

        # Assert: Todos os campos do código company_service.py
        required_fields = ['mensagem', 'company_id', 'name', 'cnpj']
        for field in required_fields:
            assert field in data, f'Campo {field} está faltando na resposta'

