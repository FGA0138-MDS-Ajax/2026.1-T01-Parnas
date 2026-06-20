"""
test_company_service_db.py - Testes de Integração do Service (Com BD Real)

Este arquivo testa a lógica do Service COM banco de dados real (SQLite em memória).
Diferença dos testes unitários:
  - SEM mocks de queries
  - Com BD REAL (em memória para testes)
  - Valida persistência de dados
  - Valida constraints do BD (unique, foreign keys, etc.)
  - Testa transações e rollback

Objetivo:
  - Testar que dados são persistidos corretamente
  - Testar constraints do BD (email único, cnpj único)
  - Testar relacionamentos (user-company)
  - Testar rollback em caso de erro

Fixtures usadas (do conftest.py):
  - app: Aplicação Flask com BD em memória
  - clean_db: Limpa BD antes de cada teste
  - test_user: Usuário de teste pré-criado
"""

import pytest
from app.services.company_service import register_company
from app.models.company import Company
from app.models.user import User
from app.config import db


class TestRegisterCompanyWithDatabase:
    """Testes com banco de dados real (em memória)"""
    
    def test_register_company_persists_to_database(self, clean_db, test_user, app_context):
        """
        CENÁRIO: Registrar empresa com dados válidos
        ESPERADO: Empresa é criada e persistida no BD
        """
        
        company_data = {
            'name': 'Empresa Teste',
            'cnpj': '11.222.333/0001-81',
            'email': 'empresa@test.com',
            'phone': '1133334444'
        }
        
        # Action
        result, status_code = register_company(test_user.user_id, company_data)
        
        # Assert: Status 201
        assert status_code == 201
        assert result['mensagem'] == 'Empresa cadastrada com sucesso'
        
        # Assert: Buscar empresa pelo ID retornado
        company_id = result['company_id']
        company = Company.query.get(company_id)
        
        assert company is not None
        assert company.name == 'Empresa Teste'
        assert company.cnpj == '11222333000181'  # Limpo
        assert company.email == 'empresa@test.com'
        assert company.phone == '1133334444'
    
    def test_register_company_creates_user_association(self, clean_db, test_user, app_context):
        """
        CENÁRIO: Registrar empresa cria associação com usuário
        ESPERADO: user.companies contém a empresa
        """
        
        company_data = {
            'name': 'Empresa do Usuário',
            'cnpj': '11.222.333/0001-81',
            'email': 'empresa_user@test.com',
            'phone': '1133334444'
        }
        
        # Action
        result, status_code = register_company(test_user.user_id, company_data)
        company_id = result['company_id']
        
        # Assert: Recarregar usuário e verificar empresas
        user = User.query.get(test_user.user_id)
        company = Company.query.get(company_id)
        
        assert len(user.companies) == 1
        assert user.companies[0].company_id == company_id
        assert company in user.companies
    
    def test_register_company_cleanup_cnpj_formatting(self, clean_db, test_user, app_context):
        """
        CENÁRIO: CNPJ formatado é limpo antes de salvar
        ESPERADO: BD contém CNPJ sem pontos, barra, hífen
        """
        
        company_data = {
            'name': 'Empresa Formatada',
            'cnpj': '11.222.333/0001-81',  # Com formatação
            'email': 'formatada@test.com',
            'phone': '1133334444'
        }
        
        # Action
        result, status_code = register_company(test_user.user_id, company_data)
        company_id = result['company_id']
        
        # Assert: CNPJ foi limpo no BD
        company = Company.query.get(company_id)
        assert company.cnpj == '11222333000181'  # Sem formatação
        assert '.' not in company.cnpj
        assert '/' not in company.cnpj
        assert '-' not in company.cnpj


class TestRegisterCompanyConstraints:
    """Testes de constraints do BD (regras de integridade)"""
    
    def test_duplicate_cnpj_rejected(self, clean_db, test_user, app_context):
        """
        CENÁRIO: Registrar duas empresas com mesmo CNPJ
        ESPERADO: Segunda tentativa falha com 409
        """
        
        company_data = {
            'name': 'Primeira Empresa',
            'cnpj': '11.222.333/0001-81',
            'email': 'primeira@test.com',
            'phone': '1133334444'
        }
        
        # Action: Primeira empresa
        result1, status1 = register_company(test_user.user_id, company_data)
        assert status1 == 201
        
        # Action: Segunda empresa com MESMO CNPJ
        company_data['name'] = 'Segunda Empresa'
        company_data['email'] = 'segunda@test.com'
        result2, status2 = register_company(test_user.user_id, company_data)
        
        # Assert: Rejeitado
        assert status2 == 409
        assert 'CNPJ já cadastrado' in result2['erro']
    
    def test_duplicate_email_rejected(self, clean_db, test_user, app_context):
        """
        CENÁRIO: Registrar duas empresas com mesmo EMAIL
        ESPERADO: Segunda tentativa falha com 500 (constraint do BD)
        """
        
        company_data = {
            'name': 'Primeira Empresa',
            'cnpj': '11.222.333/0001-81',
            'email': 'mesmo@email.com',
            'phone': '1133334444'
        }
        
        # Action: Primeira empresa
        result1, status1 = register_company(test_user.user_id, company_data)
        assert status1 == 201
        
        # Action: Segunda empresa com MESMO EMAIL
        company_data['name'] = 'Segunda Empresa'
        company_data['cnpj'] = '22.333.444/0001-92'  # CNPJ diferente
        result2, status2 = register_company(test_user.user_id, company_data)
        
        # Assert: Falha (constraint de email único)
        assert status2 == 500
        assert 'erro' in result2
    
    def test_same_user_can_register_multiple_companies(self, clean_db, test_user, app_context):
        """
        CENÁRIO: Mesmo usuário registra múltiplas empresas
        ESPERADO: Todas são criadas e associadas corretamente
        """
        
        companies_data = [
            {
                'name': 'Empresa 1',
                'cnpj': '11.222.333/0001-81',
                'email': 'empresa1@test.com',
                'phone': '1133334444'
            },
            {
                'name': 'Empresa 2',
                'cnpj': '22.333.444/0001-92',
                'email': 'empresa2@test.com',
                'phone': '1144445555'
            },
            {
                'name': 'Empresa 3',
                'cnpj': '33.444.555/0001-03',
                'email': 'empresa3@test.com',
                'phone': '1155556666'
            }
        ]
        
        # Action: Registrar 3 empresas
        company_ids = []
        for data in companies_data:
            result, status = register_company(test_user.user_id, data)
            assert status == 201
            company_ids.append(result['company_id'])
        
        # Assert: Usuário está associado a todas as 3
        user = User.query.get(test_user.user_id)
        assert len(user.companies) == 3
        
        for company_id in company_ids:
            company = Company.query.get(company_id)
            assert company is not None
            assert test_user.user_id in [u.user_id for u in company.users]


class TestRegisterCompanyMultipleUsers:
    """Testes com múltiplos usuários"""
    
    def test_different_users_same_company_name(self, clean_db, app_context):
        """
        CENÁRIO: Dois usuários registram empresas com mesmo NOME
        ESPERADO: Ambas são criadas (name não é unique com este CNPJ diferente)
        """
        
        # Criar 2 usuários
        from datetime import date
        import bcrypt
        hashed_pwd = bcrypt.hashpw('Senha@123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user1 = User(email='user1@test.com', password_hash=hashed_pwd, 
                    name='User 1', cpf='12345678901', birth_date=date(2000, 1, 1))
        user2 = User(email='user2@test.com', password_hash=hashed_pwd, 
                    name='User 2', cpf='12345678902', birth_date=date(2000, 1, 1))
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        company_data = {
            'name': 'Mesma Empresa',  # Mesmo nome!
            'cnpj': '11.222.333/0001-81',
            'email': 'empresa1@test.com',
            'phone': '1133334444'
        }
        
        # Action: User 1 registra empresa
        result1, status1 = register_company(user1.user_id, company_data)
        assert status1 == 201
        
        # Action: User 2 registra empresa com CNPJ diferente mas mesmo nome
        company_data['cnpj'] = '22.333.444/0001-92'
        company_data['email'] = 'empresa2@test.com'
        result2, status2 = register_company(user2.user_id, company_data)
        assert status2 == 201
        
        # Assert: Ambas foram criadas
        company1 = Company.query.get(result1['company_id'])
        company2 = Company.query.get(result2['company_id'])
        
        assert company1.name == 'Mesma Empresa'
        assert company2.name == 'Mesma Empresa'
        assert company1.company_id != company2.company_id


class TestRegisterCompanyRollback:
    """Testes de rollback em caso de erro"""
    
    def test_partial_failure_rollback(self, clean_db, test_user, app_context, mocker):
        """
        CENÁRIO: Erro durante a criação falha após db.session.add()
        ESPERADO: Rollback restaura estado anterior do BD
        """
        
        company_data = {
            'name': 'Empresa que Falha',
            'cnpj': '11.222.333/0001-81',
            'email': 'falha@test.com',
            'phone': '1133334444'
        }
        
        # Setup: db.session.commit() vai falhar
        original_commit = db.session.commit
        call_count = {'count': 0}
        
        def failing_commit():
            call_count['count'] += 1
            if call_count['count'] > 0:
                raise Exception('Simulated DB error')
            original_commit()
        
        mocker.patch.object(db.session, 'commit', side_effect=failing_commit)
        
        # Action: Tentar registrar empresa
        result, status = register_company(test_user.user_id, company_data)
        
        # Assert: Falhou (500)
        assert status == 500
        
        # Assert: Empresa NÃO foi persistida (rollback funcionou)
        companies = Company.query.all()
        assert len(companies) == 0


class TestRegisterCompanyResponseFormat:
    """Testes do formato de resposta da função"""
    
    def test_success_response_format(self, clean_db, test_user, app_context):
        """
        CENÁRIO: Resposta de sucesso tem formato correto
        ESPERADO: Todos os campos esperados presentes
        """
        
        company_data = {
            'name': 'Empresa ABC',
            'cnpj': '11.222.333/0001-81',
            'email': 'abc@test.com',
            'phone': '1133334444'
        }
        
        # Action
        result, status_code = register_company(test_user.user_id, company_data)
        
        # Assert: Status 201
        assert status_code == 201
        
        # Assert: Campos obrigatórios presentes
        assert 'mensagem' in result
        assert 'company_id' in result
        assert 'name' in result
        assert 'cnpj' in result
        
        # Assert: Valores corretos
        assert isinstance(result['company_id'], int)
        assert result['company_id'] > 0
        assert result['name'] == 'Empresa ABC'
        assert result['cnpj'] == '11222333000181'
    
    def test_error_response_format_duplicate_cnpj(self, clean_db, test_user, app_context):
        """
        CENÁRIO: Resposta de erro (CNPJ duplicado) tem formato correto
        ESPERADO: Campo 'erro' com mensagem descritiva
        """
        
        # Registrar primeira empresa
        first_data = {
            'name': 'Primeira',
            'cnpj': '11.222.333/0001-81',
            'email': 'primeira@test.com',
            'phone': '1133334444'
        }
        register_company(test_user.user_id, first_data)
        
        # Tentar registrar com CNPJ duplicado
        duplicate_data = {
            'name': 'Segunda',
            'cnpj': '11.222.333/0001-81',  # CNPJ igual
            'email': 'segunda@test.com',
            'phone': '1144445555'
        }
        result, status_code = register_company(test_user.user_id, duplicate_data)
        
        # Assert: Status 409
        assert status_code == 409
        
        # Assert: Tem campo 'erro'
        assert 'erro' in result
        assert 'CNPJ já cadastrado' in result['erro']

