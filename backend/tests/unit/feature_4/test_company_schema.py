"""
test_company_schema.py - Testes Unitários do Schema de Registr de Empresa

Este arquivo testa APENAS a camada de validação (Schema) do Marshmallow.
NÃO toca em banco de dados, NÃO faz requisições HTTP.
Objetivo: Validar que dados de entrada são aceitos/rejeitados corretamente.

Padrão de teste:
  1. Setup: Preparar dados de entrada
  2. Action: Chamar schema.load() ou schema.dump()
  3. Assert: Validar resultado ou exceção

Conceitos importantes:
  - schema.load(): Valida dados de entrada (JSON do request)
  - ValidationError: Exceção lançada quando dados são inválidos
  - err.messages: Dicionário com mensagens de erro por campo
"""

import pytest
from marshmallow import ValidationError
from app.schemas.company_schema import CompanyRegistrationSchema


class TestCompanySchemaValid:
    """Testes com dados VÁLIDOS - o schema deve aceitar"""

    @pytest.fixture
    def schema(self):
        """Fixture: Instancia um novo schema para cada teste"""
        return CompanyRegistrationSchema()

    def test_valid_company_data(self, schema):
        """
        CENÁRIO: Dados de empresa completamente válidos
        ESPERADO: schema.load() retorna dados sem erro
        """
        valid_data = {
            'name': 'Empresa XYZ Ltda',
            'cnpj': '11.222.333/0001-81',  # CNPJ válido (com formatação)
            'email': 'contato@empresa.com',
            'phone': '1133334444'
        }

        # Action: Carregar dados no schema
        result = schema.load(valid_data)

        # Assert: Dados foram aceitos e retornados
        assert result['name'] == 'Empresa XYZ Ltda'
        assert result['cnpj'] == '11.222.333/0001-81'
        assert result['email'] == 'contato@empresa.com'
        assert result['phone'] == '1133334444'

    def test_valid_company_with_formatted_phone(self, schema):
        """
        CENÁRIO: Telefone com formatação
        ESPERADO: Aceita telefones formatados (8 a 20 caracteres)
        """
        valid_data = {
            'name': 'Tech Company',
            'cnpj': '11.222.333/0001-81',
            'email': 'tech@empresa.com',
            'phone': '(11) 98765-4321'  # Com formatação
        }

        result = schema.load(valid_data)

        assert result['phone'] == '(11) 98765-4321'
        assert len(result['phone']) >= 8  # Valida tamanho mínimo


class TestCompanySchemaValidationErrors:
    """Testes com dados INVÁLIDOS - o schema deve rejeitar"""

    @pytest.fixture
    def schema(self):
        return CompanyRegistrationSchema()

    def test_missing_required_field_name(self, schema):
        """
        CENÁRIO: Campo 'name' está ausente
        ESPERADO: ValidationError com mensagem "Nome é obrigatório"
        """
        data_sem_name = {
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data_sem_name)

        # Verifica mensagem de erro
        assert 'name' in exc_info.value.messages
        assert 'obrigatório' in str(exc_info.value.messages['name']).lower()

    def test_missing_required_field_cnpj(self, schema):
        """CENÁRIO: CNPJ ausente - deve falhar"""
        data_sem_cnpj = {
            'name': 'Empresa Teste',
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data_sem_cnpj)

        assert 'cnpj' in exc_info.value.messages

    def test_missing_required_field_email(self, schema):
        """CENÁRIO: Email ausente - deve falhar"""
        data_sem_email = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'phone': '1133334444'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data_sem_email)

        assert 'email' in exc_info.value.messages

    def test_missing_required_field_phone(self, schema):
        """CENÁRIO: Telefone ausente - deve falhar"""
        data_sem_phone = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data_sem_phone)

        assert 'phone' in exc_info.value.messages


class TestCompanySchemaNameValidation:
    """Testes específicos para validação do campo NAME"""

    @pytest.fixture
    def schema(self):
        return CompanyRegistrationSchema()

    def test_name_empty_string(self, schema):
        """CENÁRIO: Name é string vazia - deve rejeitar"""
        data = {
            'name': '',  # Vazio!
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        assert 'name' in exc_info.value.messages

    def test_name_too_long(self, schema):
        """CENÁRIO: Name com mais de 150 caracteres - deve rejeitar"""
        long_name = 'A' * 151  # 151 caracteres (máximo é 150)
        data = {
            'name': long_name,
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        assert 'name' in exc_info.value.messages

    def test_name_exactly_150_chars(self, schema):
        """CENÁRIO: Name com exatamente 150 caracteres - deve aceitar"""
        name_150 = 'A' * 150
        data = {
            'name': name_150,
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        result = schema.load(data)
        assert result['name'] == name_150


class TestCompanySchemaEmailValidation:
    """Testes específicos para validação do campo EMAIL"""

    @pytest.fixture
    def schema(self):
        return CompanyRegistrationSchema()

    def test_invalid_email_format(self, schema):
        """CENÁRIO: Email sem @ - deve rejeitar"""
        data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'emailinvalido.com',  # Sem @
            'phone': '1133334444'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        assert 'email' in exc_info.value.messages
        assert 'inválido' in str(exc_info.value.messages['email']).lower()

    def test_valid_email_formats(self, schema):
        """CENÁRIO: Diferentes formatos válidos de email"""
        valid_emails = [
            'contato@empresa.com',
            'nome+tag@empresa.com.br',
            'usuario_teste@sub.empresa.com'
        ]

        for email in valid_emails:
            data = {
                'name': 'Empresa Teste',
                'cnpj': '11.222.333/0001-81',
                'email': email,
                'phone': '1133334444'
            }

            result = schema.load(data)
            assert result['email'] == email


class TestCompanySchemaPhoneValidation:
    """Testes específicos para validação do campo PHONE"""

    @pytest.fixture
    def schema(self):
        return CompanyRegistrationSchema()

    def test_phone_too_short(self, schema):
        """CENÁRIO: Telefone com menos de 8 caracteres - deve rejeitar"""
        data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1234567'  # Apenas 7 caracteres (mínimo é 8)
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        assert 'phone' in exc_info.value.messages

    def test_phone_too_long(self, schema):
        """CENÁRIO: Telefone com mais de 20 caracteres - deve rejeitar"""
        data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '12345678901234567890123'  # 23 caracteres (máximo é 20)
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        assert 'phone' in exc_info.value.messages

    def test_phone_exactly_8_chars(self, schema):
        """CENÁRIO: Telefone com exatamente 8 caracteres - deve aceitar"""
        data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '12345678'
        }

        result = schema.load(data)
        assert result['phone'] == '12345678'


class TestCompanySchemaNameValidation:
    """Testes específicos para validação do campo CNPJ"""

    @pytest.fixture
    def schema(self):
        return CompanyRegistrationSchema()

    def test_invalid_cnpj_format(self, schema):
        """
        CENÁRIO: CNPJ com dígitos verificadores inválidos
        ESPERADO: ValidationError com mensagem "CNPJ inválido"
        """
        data = {
            'name': 'Empresa Teste',
            'cnpj': '11.111.111/1111-11',  # CNPJ inválido (dígitos verificadores errados)
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        assert 'cnpj' in exc_info.value.messages
        assert 'inválido' in str(exc_info.value.messages['cnpj']).lower()

    def test_cnpj_too_short(self, schema):
        """CENÁRIO: CNPJ com menos de 14 caracteres - deve rejeitar"""
        data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.33',  # Muito curto
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        assert 'cnpj' in exc_info.value.messages

    def test_cnpj_too_long(self, schema):
        """CENÁRIO: CNPJ com mais de 20 caracteres - deve rejeitar"""
        data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81-EXTRA',  # Muito longo
            'email': 'teste@empresa.com',
            'phone': '1133334444'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        assert 'cnpj' in exc_info.value.messages


class TestCompanySchemaIntegration:
    """Testes de integração do schema - múltiplos campos"""

    @pytest.fixture
    def schema(self):
        return CompanyRegistrationSchema()

    def test_all_fields_invalid(self, schema):
        """CENÁRIO: Todos os campos inválidos"""
        data = {
            'name': '',
            'cnpj': 'INVALID',
            'email': 'not-an-email',
            'phone': '123'
        }

        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        # Deve ter múltiplos erros
        errors = exc_info.value.messages
        assert len(errors) >= 3  # Deve ter registros de erro para vários campos

    def test_extra_fields_are_rejected(self, schema):
        """CENÁRIO: Dados com campos extras — o schema rejeita (unknown=RAISE)"""
        data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'teste@empresa.com',
            'phone': '1133334444',
            'campo_extra': 'nao permitido',
            'outro_extra': 123
        }

        # Act: o CompanyRegistrationSchema barra campos desconhecidos
        with pytest.raises(ValidationError) as exc:
            schema.load(data)

        assert 'campo_extra' in exc.value.messages
        assert 'outro_extra' in exc.value.messages

