from unittest.mock import MagicMock
from app.services.company_service import register_company

COMPANY_DATA = {
    'name': 'Empresa Teste Ltda',
    'cnpj': '11.222.333/0001-81',
    'email': 'contato@empresa.com',
    'phone': '1133334444',
}


def _mock_deps(mocker, existing=None):
    """Mocka Company, db e user_company no módulo do service.

    `existing` é o que Company.query.filter_by(...).first() devolve
    (None = sem duplicata; um objeto = CNPJ já cadastrado).
    Retorna (company_cls, instance, db, user_company).
    """
    company_cls = mocker.patch('app.services.company_service.Company')
    company_cls.query.filter_by.return_value.first.return_value = existing
    instance = company_cls.return_value
    instance.company_id = 1
    instance.name = COMPANY_DATA['name']
    instance.cnpj = '11222333000181'

    db = mocker.patch('app.services.company_service.db')
    user_company = mocker.patch('app.services.company_service.user_company')
    return company_cls, instance, db, user_company


class TestRegisterCompanySuccess:

    def test_register_new_company_success(self, mocker):
        # Arrange: sem duplicata de CNPJ
        _mock_deps(mocker, existing=None)

        # Act
        result, status_code = register_company(1, COMPANY_DATA)

        assert status_code == 201
        assert result['mensagem'] == 'Empresa cadastrada com sucesso'
        assert result['company_id'] == 1
        assert result['name'] == COMPANY_DATA['name']

    def test_cnpj_is_cleaned_before_checking_duplicates(self, mocker):
        company_cls, _, _, _ = _mock_deps(mocker, existing=None)

        # Act: CNPJ entra formatado
        register_company(1, {**COMPANY_DATA, 'cnpj': '11.222.333/0001-81'})

        # Assert: a busca por duplicata recebe o CNPJ só com dígitos
        company_cls.query.filter_by.assert_called_once_with(cnpj='11222333000181')


class TestRegisterCompanyErrorDuplicateCNPJ:

    def test_duplicate_cnpj_returns_409(self, mocker):
        # Arrange: já existe empresa com o CNPJ
        existing = MagicMock(company_id=999)
        _, _, db, _ = _mock_deps(mocker, existing=existing)

        # Act
        result, status_code = register_company(1, COMPANY_DATA)

        assert status_code == 409
        assert 'CNPJ já cadastrado' in result['erro']
        db.session.commit.assert_not_called()


class TestRegisterCompanyErrorDatabaseException:

    def test_database_error_returns_500(self, mocker):
        _, _, db, _ = _mock_deps(mocker, existing=None)
        db.session.commit.side_effect = Exception('Database connection lost')

        # Act
        result, status_code = register_company(1, COMPANY_DATA)

        assert status_code == 500
        assert 'Ocorreu um erro interno' in result['erro']
        db.session.rollback.assert_called_once()

    def test_database_error_with_invalid_email(self, mocker):
        _, _, db, _ = _mock_deps(mocker, existing=None)
        db.session.commit.side_effect = Exception('Duplicate email')

        # Act
        result, status_code = register_company(1, {**COMPANY_DATA, 'email': 'existente@test.com'})

        assert status_code == 500
        db.session.rollback.assert_called_once()


class TestRegisterCompanyDataProcessing:

    def test_company_created_with_correct_fields(self, mocker):
        company_cls, _, _, _ = _mock_deps(mocker, existing=None)

        # Act
        register_company(1, {**COMPANY_DATA, 'name': 'Tech Company', 'email': 'tech@company.com', 'phone': '1155554444'})

        # Assert: construtor recebe os 4 campos, com CNPJ limpo
        company_cls.assert_called_once()
        kwargs = company_cls.call_args[1]
        assert kwargs['name'] == 'Tech Company'
        assert kwargs['cnpj'] == '11222333000181'
        assert kwargs['email'] == 'tech@company.com'
        assert kwargs['phone'] == '1155554444'


class TestRegisterCompanyUserAssociation:

    def test_user_company_association_created(self, mocker):
        company_cls, instance, db, user_company = _mock_deps(mocker, existing=None)
        instance.company_id = 99

        # Act
        register_company(42, COMPANY_DATA)

        # Assert: associação user-company criada com os ids corretos e executada
        user_company.insert.return_value.values.assert_called_once_with(user_id=42, company_id=99)
        db.session.execute.assert_called_once()
