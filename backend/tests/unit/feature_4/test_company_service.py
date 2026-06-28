# daniel: o service agora delega ao CompanyRepository; mocko o repositorio (nao mais
# Company/db/user_company) e o CNPJ duplicado levanta APIException em vez de retornar tupla.
from unittest.mock import MagicMock
import pytest
from app.services.company_service import register_company
from app.exceptions.api_exception import APIException

COMPANY_DATA = {
    'name': 'Empresa Teste Ltda',
    'cnpj': '11.222.333/0001-81',
    'email': 'contato@empresa.com',
    'phone': '1133334444',
}


def _mock_repo(mocker, existing=None, created=None):
    """Mocka o CompanyRepository no módulo do service.

    `existing` é o retorno de get_by_cnpj (None = sem duplicata).
    `created` é o retorno de create (a empresa recém-criada).
    """
    repo = mocker.patch('app.services.company_service.CompanyRepository')
    repo.get_by_cnpj.return_value = existing
    if created is None:
        # name é kwarg reservado do MagicMock; precisa ser setado como atributo.
        created = MagicMock(company_id=1, cnpj='11222333000181')
        created.name = COMPANY_DATA['name']
    repo.create.return_value = created
    return repo


class TestRegisterCompanySuccess:

    def test_register_new_company_success(self, mocker):
        # Arrange: sem duplicata de CNPJ
        _mock_repo(mocker, existing=None)

        # Act
        result, status_code = register_company(1, COMPANY_DATA)

        assert status_code == 201
        assert result['mensagem'] == 'Empresa cadastrada com sucesso'
        assert result['company_id'] == 1
        assert result['name'] == COMPANY_DATA['name']

    def test_cnpj_is_cleaned_before_checking_duplicates(self, mocker):
        # A limpeza do CNPJ migrou para o repositório; aqui garantimos que o service
        # delega a checagem de duplicata e a criação ao CompanyRepository.
        repo = _mock_repo(mocker, existing=None)

        register_company(42, COMPANY_DATA)

        repo.get_by_cnpj.assert_called_once_with(COMPANY_DATA['cnpj'])
        repo.create.assert_called_once_with(
            COMPANY_DATA['name'], COMPANY_DATA['cnpj'],
            COMPANY_DATA['email'], COMPANY_DATA['phone'], 42,
        )


class TestRegisterCompanyErrorDuplicateCNPJ:

    def test_duplicate_cnpj_returns_409(self, mocker):
        # Arrange: já existe empresa com o CNPJ
        repo = _mock_repo(mocker, existing=MagicMock(company_id=999))

        # Act / Assert: levanta APIException 409 e não tenta criar
        with pytest.raises(APIException) as exc:
            register_company(1, COMPANY_DATA)

        assert exc.value.status_code == 409
        assert 'CNPJ já cadastrado' in exc.value.message
        repo.create.assert_not_called()


class TestRegisterCompanyErrorDatabaseException:

    def test_database_error_returns_500(self, mocker):
        repo = _mock_repo(mocker, existing=None)
        repo.create.side_effect = Exception('Database connection lost')
        db = mocker.patch('app.services.company_service.db')

        # Act
        result, status_code = register_company(1, COMPANY_DATA)

        assert status_code == 500
        assert 'Ocorreu um erro interno' in result['erro']
        db.session.rollback.assert_called_once()

    def test_database_error_with_invalid_email(self, mocker):
        repo = _mock_repo(mocker, existing=None)
        repo.create.side_effect = Exception('Duplicate email')
        db = mocker.patch('app.services.company_service.db')

        # Act
        result, status_code = register_company(1, {**COMPANY_DATA, 'email': 'existente@test.com'})

        assert status_code == 500
        db.session.rollback.assert_called_once()


class TestRegisterCompanyDataProcessing:

    def test_company_created_with_correct_fields(self, mocker):
        repo = _mock_repo(mocker, existing=None)

        # Act
        register_company(1, {**COMPANY_DATA, 'name': 'Tech Company', 'email': 'tech@company.com', 'phone': '1155554444'})

        # Assert: o create recebe os 4 campos e o user_id
        repo.create.assert_called_once_with(
            'Tech Company', COMPANY_DATA['cnpj'], 'tech@company.com', '1155554444', 1,
        )


class TestRegisterCompanyUserAssociation:

    def test_user_company_association_created(self, mocker):
        repo = _mock_repo(mocker, existing=None)

        # Act
        register_company(42, COMPANY_DATA)

        # Assert: a associação user-company é responsabilidade do repositório;
        # o service repassa o user_id correto para o create.
        assert repo.create.call_args[0][4] == 42
