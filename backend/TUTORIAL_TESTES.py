"""
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║     TUTORIAL COMPLETO: TESTANDO A FEATURE DE CADASTRO DE EMPRESA COM PYTEST       ║
║                                                                                    ║
║  Um guia prático para aprender a estruturar e escrever testes em diferentes       ║
║  camadas: Schema, Service, Routes, Integração e End-to-End (E2E)                  ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝


📚 ÍNDICE DO TUTORIAL
═══════════════════════════════════════════════════════════════════════════════════

1. CONCEITOS FUNDAMENTAIS
   1.1 O que é pytest?
   1.2 Estrutura de testes (Arrange, Act, Assert)
   1.3 Tipos de testes (unitários, integração, E2E)
   1.4 Fixtures

2. ROTEIRO ESTRUTURADO DE TESTES
   2.1 Schema Layer (Testes Unitários)
   2.2 Service Layer (Testes com Mocks)
   2.3 Service Layer (Testes com BD Reaal)
   2.4 Route/API Layer (Testes HTTP)
   2.5 End-to-End (Testes de Fluxo Completo)

3. COMO EXECUTAR OS TESTES
   3.1 Executar todos os testes
   3.2 Executar apenas categorias específicas
   3.3 Ver cobertura de código
   3.4 Debug de testes falhando

4. MÓS PRÁTICAS E PADRÕES

5. COMO ADICIONAR NOVOS TESTES


═══════════════════════════════════════════════════════════════════════════════════
1. CONCEITOS FUNDAMENTAIS
═══════════════════════════════════════════════════════════════════════════════════

🔹 O que é pytest?
──────────────────
Pytest é um framework de testes para Python. Ele:
  - Descobre testes automaticamente (funções test_*.py)
  - Fornece fixtures para compartilhar setup entre testes
  - Oferece várias plugins e extensões
  - Gera relatórios detalhados

Exemplo simples:
    def test_soma():
        resultado = 2 + 2
        assert resultado == 4


🔹 Estrutura de Testes (Arrange, Act, Assert)
───────────────────────────────────────────────
Cada teste segue 3 fases:

1. ARRANGE (Setup): Preparar dados e dependências
    user = User(email='teste@test.com', ...)
    db.session.add(user)
    db.session.commit()

2. ACT (Action): Executar o código sendo testado
    result, status_code = register_company(user.user_id, company_data)

3. ASSERT (Verificação): Validar que o resultado é correto
    assert status_code == 201
    assert result['company_id'] > 0


🔹 Tipos de Testes
─────────────────

TESTES UNITÁRIOS (Unit Tests)
  → Testam UMA função/método isolada
  → Usam MOCKS para dependências externas
  → Não tocam em BD, HTTP, arquivos
  → Rápidos e focados

  Exemplo: Testar lógica de limpeza de CNPJ
    def clean_cnpj(cnpj):
        return re.sub(r'\D', '', cnpj)

    assert clean_cnpj('11.222.333/0001-81') == '11222333000181'


TESTES DE INTEGRAÇÃO (Integration Tests)
  → Testam múltiplos componentes juntos
  → Usam BD REAL (em memória para testes)
  → Validam persistência e constraints
  → Mais lentos que unitários

  Exemplo: Testar que empresa é salva corretamente no BD


TESTES END-TO-END (E2E Tests)
  → Testam fluxo COMPLETO como usuário real
  → Múltiplos endpoints HTTP em sequência
  → Validam efeitos colaterais de ponta a ponta
  → Mais lentos, mas mais realísticos

  Exemplo: Login → Cadastro de Empresa → Verificação


🔹 Fixtures (Reutilizar Setup)
──────────────────────────────

Fixtures são "funções de setup" reutilizáveis que pytest fornece.

Exemplo sem fixture (repetitivo):
    def test_1():
        user = User(email='...')
        db.session.add(user)
        db.session.commit()
        # ... teste

    def test_2():
        user = User(email='...')  # REPETIÇÃO!
        db.session.add(user)
        db.session.commit()
        # ... teste


Exemplo com fixture (DRY):
    @pytest.fixture
    def test_user(app_context):
        user = User(email='...')
        db.session.add(user)
        db.session.commit()
        return user

    def test_1(test_user):  # Usa fixture
        assert test_user is not None

    def test_2(test_user):  # Reutiliza fixture
        assert test_user.email == '...'


═══════════════════════════════════════════════════════════════════════════════════
2. ROTEIRO ESTRUTURADO DE TESTES
═══════════════════════════════════════════════════════════════════════════════════

O roteiro abaixo segue a arquitetura em camadas do seu projeto:

REQUEST HTTP
    ↓
[ROUTE LAYER] ← Valida JWT, recebe JSON
    ↓
[SCHEMA LAYER] ← Valida dados com Marshmallow
    ↓
[SERVICE LAYER] ← Lógica de negócio
    ↓
[DATABASE] ← Persiste dados


🔹 CAMADA 1: SCHEMA LAYER (Testes Unitários)
──────────────────────────────────────────────

Arquivo: tests/unit/test_company_schema.py

O que testar:
  ✓ Campos obrigatórios presentes
  ✓ Validação de tamanho (min/max)
  ✓ Validação de email (formato)
  ✓ Validação de CNPJ (dígitos verificadores)
  ✗ Dados inválidos são rejeitados com erro descritivo

Como testar:
    from app.schemas.company_schema import CompanyRegistrationSchema

    def test_valid_company():
        schema = CompanyRegistrationSchema()
        data = {
            'name': 'Empresa',
            'cnpj': '11.222.333/0001-81',
            'email': 'empresa@test.com',
            'phone': '1133334444'
        }
        result = schema.load(data)
        assert result['name'] == 'Empresa'

    def test_invalid_email():
        schema = CompanyRegistrationSchema()
        data = {..., 'email': 'invalid-email', ...}
        with pytest.raises(ValidationError) as exc:
            schema.load(data)
        assert 'email' in exc.value.messages

Executar:
    pytest tests/unit/test_company_schema.py -v


🔹 CAMADA 2: SERVICE LAYER (Testes Unitários com Mocks)
─────────────────────────────────────────────────────────

Arquivo: tests/unit/test_company_service.py

O que testar:
  ✓ Limpeza de CNPJ (remove formatação)
  ✓ Verificação de CNPJ duplicado (mock query)
  ✓ Criação de objeto Company
  ✓ Associação user-company
  ✗ Tratamento de exceção em erro de BD

Como testar (com mocks):
    from unittest.mock import MagicMock
    from app.services.company_service import register_company

    def test_duplicate_cnpj(mocker):
        # Setup: Mock da query
        existing = MagicMock()
        existing.company_id = 999

        mocker.patch(
            'app.services.company_service.Company.query.filter_by',
            return_value=MagicMock(first=MagicMock(return_value=existing))
        )

        # Action
        result, status = register_company(user_id=1, data={...})

        # Assert
        assert status == 409
        assert 'CNPJ já cadastrado' in result['erro']

Quando usar MagicMock:
  - Não quer chamar BD real
  - Quer simular comportamentos específicos
  - Quer verificar que funções foram chamadas corretamente

Executar:
    pytest tests/unit/test_company_service.py -v


🔹 CAMADA 3: SERVICE LAYER (Testes com BD Real)
─────────────────────────────────────────────────

Arquivo: tests/integration/test_company_service_db.py

O que testar:
  ✓ Dados persistem no BD
  ✓ Associação user-company é criada
  ✓ CNPJ único enforce (constraint do BD)
  ✓ Email único enforce (constraint do BD)
  ✓ Rollback em erro

Como testar:
    def test_company_persists(clean_db, test_user, app_context):
        # Usa BD REAL (em memória)
        company_data = {...}
        result, status = register_company(test_user.user_id, company_data)

        # Buscar empresa no BD e validar
        company = Company.query.get(result['company_id'])
        assert company.name == 'Empresa'
        assert company.cnpj == '11222333000181'

    def test_duplicate_cnpj_in_db(clean_db, test_user, app_context):
        # Primeira empresa
        register_company(test_user.user_id, {..., 'cnpj': '11....')

        # Segunda com CNPJ único - deve falhar no BD
        result2, status2 = register_company(test_user.user_id, {..., 'cnpj': '11....'})
        assert status2 == 409

Diferenças vs. testes com mock:
  • NÃO usa mocks de queries
  • Usa BD SQLite em memória (rápido)
  • Testa constraints reais do BD
  • Mais realista, um pouco mais lento

Executar:
    pytest tests/integration/test_company_service_db.py -v


🔹 CAMADA 4: ROUTE LAYER (Testes de APIs HTTP)
────────────────────────────────────────────────

Arquivo: tests/integration/test_company_routes.py

O que testar:
  ✓ Rotas sem JWT retornam 401
  ✓ Rotas com JWT válido permitem acesso
  ✓ Dados inválidos retornam 400 com erro de schema
  ✓ Request válida retorna 201 com dados corretos
  ✓ CNPJ duplicado retorna 409
  ✓ Formato JSON correto na resposta

Como testar (HTTPClient):
    def test_register_with_jwt(client, clean_db, auth_headers, test_user):
        # auth_headers = {'Authorization': 'Bearer TOKEN', 'Content-Type': 'application/json'}

        response = client.post(
            '/api/companies/register',
            json={
                'name': 'Empresa',
                'cnpj': '11.222.333/0001-81',
                'email': 'empresa@test.com',
                'phone': '1133334444'
            },
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.get_json()
        assert 'company_id' in data

    def test_without_jwt_returns_401(client, clean_db):
        response = client.post(
            '/api/companies/register',
            json={...},
            headers={'Content-Type': 'application/json'}  # SEM Authorization
        )

        assert response.status_code == 401

Testando com cliente HTTP:
  • client.post(endpoint, json=data, headers=headers)
  • response.status_code
  • response.get_json()
  • response.headers

Executar:
    pytest tests/integration/test_company_routes.py -v


🔹 CAMADA 5: END-TO-END (Fluxo Completo)
──────────────────────────────────────────

Arquivo: tests/e2e/test_company_registration_flow.py

O que testar:
  ✓ Usuário faz login → recebe token
  ✓ Usuário usa token para cadastrar empresa
  ✓ Empresa persiste no BD
  ✓ Usuário-empresa ficam associados
  ✓ Fluxo completo: Login → Cadastro → Verificação

Como testar (Fluxo completo):
    def test_full_flow(client, clean_db, app_context):
        # PASSO 1: Login
        login_resp = client.post(
            '/auth/login',
            json={'email': 'user@test.com', 'password': 'Senha@123'}
        )
        token = login_resp.get_json()['token']

        # PASSO 2: Registrar empresa
        response = client.post(
            '/api/companies/register',
            json={...},
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        )

        # PASSO 3: Verificar BD
        company = Company.query.get(response.get_json()['company_id'])
        assert company is not None

Executar:
    pytest tests/e2e/test_company_registration_flow.py -v


═══════════════════════════════════════════════════════════════════════════════════
3. COMO EXECUTAR OS TESTES
═══════════════════════════════════════════════════════════════════════════════════

🔹 Executar TODOS os testes
──────────────────────────

    pytest

    # Ou com mais detalhes:
    pytest -v

    # Com output de print() durante testes:
    pytest -s


🔹 Executar apenas UMA CATEGORIA
─────────────────────────────────

    # Apenas testes unitários
    pytest tests/unit/ -v

    # Apenas testes de integração
    pytest tests/integration/ -v

    # Apenas testes E2E
    pytest tests/e2e/ -v


🔹 Executar apenas UM ARQUIVO
───────────────────────────────

    pytest tests/unit/test_company_schema.py -v

    # Apenas UMA classe de testes
    pytest tests/unit/test_company_schema.py::TestCompanySchemaValid -v

    # Apenas UM teste específico
    pytest tests/unit/test_company_schema.py::TestCompanySchemaValid::test_valid_company_data -v


🔹 VER COBERTURA DE CÓDIGO
────────────────────────────

Cobertura = Quantas linhas do seu código foram executadas durante os testes.

Instalar:
    pip install pytest-cov

Executar:
    pytest --cov=app --cov-report=html

    # Gera arquivo: htmlcov/index.html (abrir no navegador)


🔹 DEBUG de TESTES FALHANDO
────────────────────────────

Quando um teste falha, use -vv para mais detalhes:
    pytest tests/unit/test_company_schema.py::TestCompanySchemaValid::test_valid_company_data -vv

Usar pdb (debugger) dentro de um teste:
    def test_exemplo():
        resultado = funcao_misteriosa()
        breakpoint()  # Pausa a execução aqui
        assert resultado == esperado


Executar apenas testes que falharam da última vez:
    pytest --lf

Executar com modo "fail fast" (para no primeiro erro):
    pytest -x


═══════════════════════════════════════════════════════════════════════════════════
4. MELHORES PRÁTICAS E PADRÕES
═══════════════════════════════════════════════════════════════════════════════════

✅ NOMES DESCRITIVOS
────────────────────
Ruim:  def test_1():
Bom:   def test_register_company_with_duplicate_cnpj_returns_409():

Padrão: test_{funcionalidade}_{cenário}_{resultado_esperado}


✅ DOCSTRINGS EXPLICATIVAS
──────────────────────────

    def test_register_duplicate_cnpj(clean_db, test_user):
        \"\"\"
        CENÁRIO: Registrar empresa com CNPJ que já existe
        ESPERADO: Status 409, mensagem 'CNPJ já cadastrado'
        \"\"\"
        # ... código do teste


✅ USE FIXTURES PARA REUTILIZAR SETUP
────────────────────────────────────

Ao invés de repetir:
    def test_1(clean_db, test_user, auth_headers):
    def test_2(clean_db, test_user, auth_headers):
    def test_3(clean_db, test_user, auth_headers):

Fixtures (conftest.py) cuidam disso automaticamente!


✅ ORGANIZE TESTES EM CLASSES
─────────────────────────────

    class TestCompanySchemaValid:
        def test_valid_data(self, schema):
            ...
        def test_another(self, schema):
            ...

    class TestCompanySchemaErros:
        def test_missing_field(self, schema):
            ...


✅ USE ASSERT COM MENSAGENS
──────────────────────────

    assert result == esperado
    assert result == esperado, f'Esperado {esperado}, got {result}'

    # Pytest mostra a diferença automaticamente


✅ TESTE UM CENÁRIO POR TESTE
────────────────────────────

Ruim:
    def test_company():
        # testa válido
        # testa inválido
        # testa duplicado
        # testa 5 coisas...

Bom:
    def test_valid_company():
        # testa válido

    def test_invalid_company():
        # testa inválido

    def test_duplicate_company():
        # testa duplicado


═══════════════════════════════════════════════════════════════════════════════════
5. COMO ADICIONAR NOVOS TESTES
═══════════════════════════════════════════════════════════════════════════════════

Passo a passo para adicionar um novo teste:

1️⃣ IDENTIFIQUE O CENÁRIO
   "Preciso testar que empresa com email duplicado é rejeitada"

2️⃣ ESCOLHA A CAMADA
   - Schema? Serviço? BD? HTTP? E2E?

   Neste caso:
   - Schema valida EMAIL? SIM → Teste em test_company_schema.py
   - Service verifica duplicado? NÃO → Não precisa lá
   - BD tem constraint? SIM → Adicione em test_company_service_db.py
   - HTTP retorna 500? SIM → Adicione em test_company_routes.py

3️⃣ ESCREVA O TESTE SEGUINDO O PADRÃO

   def test_duplicate_email_in_bd(clean_db, test_user, app_context):
       \"\"\"
       CENÁRIO: Registrar duas empresas com mesmo EMAIL
       ESPERADO: Segunda falha (constraint de BD)
       \"\"\"

       # Arrange
       empresa1 = {..., 'email': 'mesmo@email.com'}
       empresa2 = {..., 'email': 'mesmo@email.com'}

       # Act
       resultado1 = register_company(test_user.user_id, empresa1)
       resultado2 = register_company(test_user.user_id, empresa2)

       # Assert
       assert resultado1[1] == 201
       assert resultado2[1] == 500  # Erro do BD

4️⃣ EXECUTE E VALIDE

   pytest tests/integration/test_company_service_db.py::test_duplicate_email_in_bd -v

   Teste passa? Ótimo! Se não, debug até funcionar.


═══════════════════════════════════════════════════════════════════════════════════
RESUMO - CHECKLIST DE TESTES MÍNIMO PARA FEATURE DE CADASTRO
═══════════════════════════════════════════════════════════════════════════════════

SCHEMA (tests/unit/test_company_schema.py):
  ☐ Dados válidos são aceitos
  ☐ Campos obrigatórios validam
  ☐ Email inválido é rejeitado
  ☐ CNPJ inválido é rejeitado
  ☐ Tamanho mínimo/máximo de campos

SERVICE - UNITÁRIO (tests/unit/test_company_service.py):
  ☐ Limpeza de CNPJ funciona
  ☐ CNPJ duplicado retorna 409
  ☐ Dados são criados corretamente
  ☐ Erro de BD retorna 500 com rollback

SERVICE - INTEGRAÇÃO (tests/integration/test_company_service_db.py):
  ☐ Empresa persiste no BD
  ☐ Associação user-company é criada
  ☐ CNPJ único é enforçado
  ☐ Email único é enforçado

ROUTES (tests/integration/test_company_routes.py):
  ☐ Sem JWT retorna 401
  ☐ Com JWT válido funciona
  ☐ Dados inválidos retornam 400
  ☐ Sucesso retorna 201
  ☐ CNPJ duplicado retorna 409

E2E (tests/e2e/test_company_registration_flow.py):
  ☐ Fluxo completo: login → cadastro → verificação


═══════════════════════════════════════════════════════════════════════════════════
PRÓXIMAS DICAS
═══════════════════════════════════════════════════════════════════════════════════

1. Execute os testes agora:
   cd backend
   pytest tests/ -v

2. Se algum teste falhar, use -vv para mais detalhes
   pytest tests/ -vv

3. Veja a cobertura:
   pytest --cov=app --cov-report=html
   # Abra htmlcov/index.html

4. Adicione novos testes para funcionalidades novas

5. Use 'pytest -x' para parar no primeiro erro (útil para debug)


Happy testing! 🚀
"""

print(__doc__)

