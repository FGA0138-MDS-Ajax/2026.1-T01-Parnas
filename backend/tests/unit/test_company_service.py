"""
test_company_service.py - Testes Unitários do Service de Empresa

Este arquivo testa APENAS a lógica de negócio do Service.
Usa MOCKS para simular banco de dados e dependências.
NÃO toca em banco de dados real, NÃO faz requisições HTTP.

Objetivo: Testar lógica isolada de:
  - Verificação de CNPJ duplicado
  - Limpeza de CNPJ
  - Criação de objeto Company
  - Tratamento de exceções

Padrão de teste com mocks:
  1. Setup: Mock dependências (DB, queries)
  2. Action: Chamar função do service
  3. Assert: Validar resultado e comportamento esperado

Conceitos:
  - mocker.patch(): Substitui uma função/classe por um mock
  - Mock.return_value: Define o retorno da função mockada
  - Mock.side_effect: Faz a função lancarpException ou comportamento customizado
  - MagicMock: Cria um objeto fake que aceita qualquer método/atributo
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from app.services.company_service import register_company


class TestRegisterCompanySuccess:
    """Testes de SUCESSO - empresa é registrada com sucesso"""

    def test_register_new_company_success(self, mocker):
        """
        CENÁRIO: Registrar empresa nova com dados válidos
        ESPERADO: Status 201, retorna dados da empresa

        Passo a passo:
        1. Mock das queries do BD
        2. Mock da sessão do BD
        3. Chama register_company()
        4. Valida resultado
        """

        # Setup: Dados de entrada
        user_id = 1
        company_data = {
            'name': 'Empresa Teste Ltda',
            'cnpj': '11.222.333/0001-81',
            'email': 'contato@empresa.com',
            'phone': '1133334444'
        }

        # Setup: Mock do modelo Company
        mock_company = MagicMock()
        mock_company.company_id = 1
        mock_company.name = 'Empresa Teste Ltda'
        mock_company.cnpj = '11222333000181'  # Limpo (sem formatação)

        # Setup: Mock da query que verifica CNPJ duplicado
        # Simula: Company.query.filter_by(cnpj=...).first() retorna None (não existe)
        mocker.patch(
            'app.services.company_service.Company.query.filter_by',
            return_value=MagicMock(first=MagicMock(return_value=None))
        )

        # Setup: Mock do Model Company (construtor)
        mocker.patch(
            'app.services.company_service.Company',
            return_value=mock_company
        )

        # Setup: Mock do banco de dados (db.session)
        mock_db_session = MagicMock()
        mocker.patch('app.services.company_service.db.session', mock_db_session)

        # Setup: Mock do user_company (many-to-many)
        mock_insert = MagicMock()
        mock_insert.values = MagicMock(return_value=MagicMock())
        mocker.patch(
            'app.services.company_service.user_company.insert',
            return_value=mock_insert
        )

        # Action: Chamar função
        result, status_code = register_company(user_id, company_data)

        # Assert: Validar resultado
        assert status_code == 201
        assert result['mensagem'] == 'Empresa cadastrada com sucesso'
        assert result['company_id'] == 1
        assert result['name'] == 'Empresa Teste Ltda'

        # Assert: Validar que db.session.commit() foi chamado
        mock_db_session.commit.assert_called_once()

    def test_cnpj_is_cleaned_before_checking_duplicates(self, mocker):
        """
        CENÁRIO: CNPJ formatado é limpo antes de verificar duplicata
        ESPERADO: Remove caracteres não-numéricos (pontos, barra, hífen)

        Exemplo:
        - Input: '11.222.333/0001-81'
        - Limpo: '11222333000181'
        """

        user_id = 1
        company_data = {
            'name': 'Empresa',
            'cnpj': '11.222.333/0001-81',  # Com formatação
            'email': 'empresa@test.com',
            'phone': '1133334444'
        }

        # Setup: Capturar o CNPJ que foi passado para a query
        captured_cnpj = None

        def capture_filter_by(cnpj):
            nonlocal captured_cnpj
            captured_cnpj = cnpj
            return MagicMock(first=MagicMock(return_value=None))

        mock_company = MagicMock()
        mock_company.company_id = 1

        mocker.patch(
            'app.services.company_service.Company.query.filter_by',
            side_effect=capture_filter_by
        )
        mocker.patch(
            'app.services.company_service.Company',
            return_value=mock_company
        )
        mocker.patch('app.services.company_service.db.session', MagicMock())
        mocker.patch(
            'app.services.company_service.user_company.insert',
            return_value=MagicMock(values=MagicMock(return_value=MagicMock()))
        )

        # Action
        register_company(user_id, company_data)

        # Assert: CNPJ foi limpo (sem pontos, barra, hífen)
        assert captured_cnpj == '11222333000181'
        assert '.' not in captured_cnpj
        assert '/' not in captured_cnpj
        assert '-' not in captured_cnpj


class TestRegisterCompanyErrorDuplicateCNPJ:
    """Testes de ERRO - CNPJ já existe"""

    def test_duplicate_cnpj_returns_409(self, mocker):
        """
        CENÁRIO: Tentar registrar com CNPJ que já existe no BD
        ESPERADO: Status 409 (Conflict), mensagem de erro
        """

        user_id = 1
        company_data = {
            'name': 'Nova Empresa',
            'cnpj': '11.222.333/0001-81',
            'email': 'nova@test.com',
            'phone': '1133334444'
        }

        # Setup: Simular que CNPJ já existe (query retorna uma empresa)
        existing_company = MagicMock()
        existing_company.company_id = 999
        existing_company.name = 'Empresa Existente'

        mocker.patch(
            'app.services.company_service.Company.query.filter_by',
            return_value=MagicMock(first=MagicMock(return_value=existing_company))
        )

        # Setup: Mock do db.session (não deve ser usado neste cenário)
        mock_db_session = MagicMock()
        mocker.patch('app.services.company_service.db.session', mock_db_session)

        # Action
        result, status_code = register_company(user_id, company_data)

        # Assert
        assert status_code == 409
        assert 'erro' in result
        assert 'CNPJ já cadastrado' in result['erro']

        # db.session.commit() não deve ser chamado
        mock_db_session.commit.assert_not_called()


class TestRegisterCompanyErrorDatabaseException:
    """Testes de ERRO - Exceção no banco de dados"""

    def test_database_error_returns_500(self, mocker):
        """
        CENÁRIO: Ocorre exceção ao salvar no BD
        ESPERADO: Status 500, mensagem de erro, rollback

        Exemplos de erro:
        - Conexão perdida com BD
        - Constraint violation (email duplicado)
        - Timeout
        """

        user_id = 1
        company_data = {
            'name': 'Empresa',
            'cnpj': '11.222.333/0001-81',
            'email': 'empresa@test.com',
            'phone': '1133334444'
        }

        # Setup: CNPJ não duplicado (passa na primeira verificação)
        mocker.patch(
            'app.services.company_service.Company.query.filter_by',
            return_value=MagicMock(first=MagicMock(return_value=None))
        )

        # Setup: Company é criado, mas...
        mock_company = MagicMock()
        mocker.patch(
            'app.services.company_service.Company',
            return_value=mock_company
        )

        # Setup: db.session.commit() LANÇA exceção
        mock_db_session = MagicMock()
        mock_db_session.commit.side_effect = Exception('Database connection lost')
        mocker.patch('app.services.company_service.db.session', mock_db_session)

        mocker.patch(
            'app.services.company_service.user_company.insert',
            return_value=MagicMock(values=MagicMock(return_value=MagicMock()))
        )

        # Action
        result, status_code = register_company(user_id, company_data)

        # Assert
        assert status_code == 500
        assert 'erro' in result
        assert 'Ocorreu um erro interno' in result['erro']

        # Deve ter feito rollback
        mock_db_session.rollback.assert_called_once()

    def test_database_error_with_invalid_email(self, mocker):
        """
        CENÁRIO: Email já existe (constraint de email único no BD)
        ESPERADO: Status 500, erro capturado
        """

        user_id = 1
        company_data = {
            'name': 'Empresa Nova',
            'cnpj': '11.222.333/0001-81',
            'email': 'email_existente@test.com',  # Email já está em uso
            'phone': '1133334444'
        }

        # Setup: CNPJ não duplicado
        mocker.patch(
            'app.services.company_service.Company.query.filter_by',
            return_value=MagicMock(first=MagicMock(return_value=None))
        )

        # Setup: Company é criado, mas...
        mock_company = MagicMock()
        mocker.patch(
            'app.services.company_service.Company',
            return_value=mock_company
        )

        # Setup: db.session.commit() lança erro de email duplicado
        mock_db_session = MagicMock()
        mock_db_session.commit.side_effect = Exception('Duplicate email')
        mocker.patch('app.services.company_service.db.session', mock_db_session)

        mocker.patch(
            'app.services.company_service.user_company.insert',
            return_value=MagicMock(values=MagicMock(return_value=MagicMock()))
        )

        # Action
        result, status_code = register_company(user_id, company_data)

        # Assert
        assert status_code == 500
        mock_db_session.rollback.assert_called_once()


class TestRegisterCompanyDataProcessing:
    """Testes da manipulação de dados"""

    def test_company_created_with_correct_fields(self, mocker):
        """
        CENÁRIO: Verificar que objeto Company é criado com dados corretos
        ESPERADO: Construtor Company() recebe os 4 campos corretos
        """

        user_id = 1
        company_data = {
            'name': 'Tech Company',
            'cnpj': '11.222.333/0001-81',
            'email': 'tech@company.com',
            'phone': '1155554444'
        }

        # Setup
        mocker.patch(
            'app.services.company_service.Company.query.filter_by',
            return_value=MagicMock(first=MagicMock(return_value=None))
        )

        mock_company = MagicMock()
        mock_company.company_id = 1
        mock_company_constructor = mocker.patch(
            'app.services.company_service.Company',
            return_value=mock_company
        )

        mocker.patch('app.services.company_service.db.session', MagicMock())
        mocker.patch(
            'app.services.company_service.user_company.insert',
            return_value=MagicMock(values=MagicMock(return_value=MagicMock()))
        )

        # Action
        register_company(user_id, company_data)

        # Assert: Verifica argumentos passados ao construtor Company
        mock_company_constructor.assert_called_once()
        call_kwargs = mock_company_constructor.call_args[1]

        assert call_kwargs['name'] == 'Tech Company'
        assert call_kwargs['cnpj'] == '11222333000181'  # Limpo
        assert call_kwargs['email'] == 'tech@company.com'
        assert call_kwargs['phone'] == '1155554444'


class TestRegisterCompanyUserAssociation:
    """Testes da criação de associação user-company"""

    def test_user_company_association_created(self, mocker):
        """
        CENÁRIO: Verificar que associação user-company é criada
        ESPERADO: user_company.insert().values(user_id=..., company_id=...) é chamado
        """

        user_id = 42
        company_data = {
            'name': 'Empresa',
            'cnpj': '11.222.333/0001-81',
            'email': 'empresa@test.com',
            'phone': '1133334444'
        }

        # Setup
        mocker.patch(
            'app.services.company_service.Company.query.filter_by',
            return_value=MagicMock(first=MagicMock(return_value=None))
        )

        mock_company = MagicMock()
        mock_company.company_id = 99
        mocker.patch(
            'app.services.company_service.Company',
            return_value=mock_company
        )

        mock_db_session = MagicMock()
        mocker.patch('app.services.company_service.db.session', mock_db_session)

        mock_insert = MagicMock()
        mock_values = MagicMock()
        mock_insert.values = MagicMock(return_value=mock_values)

        mock_user_company_insert = mocker.patch(
            'app.services.company_service.user_company.insert',
            return_value=mock_insert
        )

        # Action
        register_company(user_id, company_data)

        # Assert: Verifica que user_company.insert().values() foi chamado certo
        mock_user_company_insert.assert_called_once()
        mock_insert.values.assert_called_once_with(
            user_id=42,
            company_id=99
        )

        # db.session.execute() deve ser chamado com o resultado
        mock_db_session.execute.assert_called_once_with(mock_values)

