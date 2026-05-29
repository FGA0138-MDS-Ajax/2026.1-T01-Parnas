#!/usr/bin/env python
"""
╔════════════════════════════════════════════════════════════════════════════════════╗
║                   GUIA RÁPIDO - COMO EXECUTAR OS TESTES                           ║
║                         (Copie e cole os comandos)                                ║
╚════════════════════════════════════════════════════════════════════════════════════╝
"""

print("""

█████████████████████████████████████████████████████████████████████████████████████
                            🚀 COMECE AQUI
█████████████████████████████████████████████████████████████████████████████████████

1️⃣ RODAR TODOS OS TESTES (RECOMENDADO PRIMEIRO):

   pytest tests/ -v

   Resultado esperado: ~45 testes ✅ passando


2️⃣ RODAR TESTES QUE JÁ PASSAM (Para praticar):

   # Schema (validação) - 20 TESTES ✅
   pytest tests/unit/test_company_schema.py -v

   # Service com BD - 9 TESTES ✅
   pytest tests/integration/test_company_service_db.py -v

   # Routes HTTP - algumas funcionando
   pytest tests/integration/test_company_routes.py::TestCompanyRoutesSuccess -v


3️⃣ ENTENDER ESTRUTURA:

   # Ver quantos testes cada arquivo tem
   pytest tests/ --collect-only -q

   # Rodar com resumido
   pytest tests/ -q


█████████████████████████████████████████████████████████████████████████████████████
                         📚 APRENDER (Tutoriais)
█████████████████████████████████████████████████████████████████████████████████████

Abra e leia estes arquivos:

  1. TUTORIAL_TESTES.py
      → Aprenda detalhadamente cada tipo de teste
      → Com explicações e exemplos

  2. RESUMO_TESTES.py
      → Veja estatísticas e próximos passos

  3. tests/conftest.py
      → Entenda como as fixtures funcionam

  4. tests/unit/test_company_schema.py
      → Veja exemplos de testes unitários


█████████████████████████████████████████████████████████████████████████████████████
                    🔍 DEBUG E VER O QUE ESTÁ ACONTECENDO
█████████████████████████████████████████████████████████████████████████████████████

# Ver prints durante testes
pytest tests/unit/test_company_schema.py::TestCompanySchemaValid -v -s

# Ver mais detalhes de erro
pytest tests/unit/test_company_schema.py::TestCompanySchemaValid::test_valid_company_data -vv

# Parar no primeiro erro
pytest tests/ -x

# Rodar apenas testes que falharam última vez
pytest tests/ --lf


█████████████████████████████████████████████████████████████████████████████████████
                        📊 VER COBERTURA DE CÓDIGO
█████████████████████████████████████████████████████████████████████████████████████

# Simples (% de cobertura)
pytest tests/ --cov=app

# Gera relatório em HTML (abra htmlcov/index.html)
pytest tests/ --cov=app --cov-report=html

# Com detalhes
pytest tests/ --cov=app --cov-report=term-missing


█████████████████████████████████████████████████████████████████████████████████████
                      🎯 EXECUTAR TESTES ESPECÍFICOS
█████████████████████████████████████████████████████████████████████████████████████

# Uma classe de testes
pytest tests/unit/test_company_schema.py::TestCompanySchemaValid -v

# Um teste específico
pytest tests/unit/test_company_schema.py::TestCompanySchemaValid::test_valid_company_data -v

# Testes com palavra 'cnpj' no nome
pytest tests/unit/test_company_schema.py -k cnpj -v

# Testes EXCETO os com palavra 'error'
pytest tests/unit/test_company_schema.py -k "not error" -v

# Apenas testes unitários
pytest tests/unit/ -v

# Apenas integração
pytest tests/integration/ -v

# Apenas E2E
pytest tests/e2e/ -v


█████████████████████████████████████████████████████████████████████████████████████
                     💡 EXPLORAR E APRENDER
█████████████████████████████████████████████████████████████████████████████████████

1. Leia o TUTORIAL_TESTES.py para entender conceitos

2. Execute um teste simples e veja passar:
   pytest tests/unit/test_company_schema.py::TestCompanySchemaValid::test_valid_company_data -vv -s

3. Mude um teste propositalmente para falhar:
   Abra tests/unit/test_company_schema.py
   Mude: assert result['name'] == 'Empresa XYZ Ltda'
   Para: assert result['name'] == 'Outro Nome'
   Execute: pytest ...
   Veja falhar, entenda por quê

4. Corrija e faça passar novamente

5. Leia os comentários em cada arquivo de teste


█████████████████████████████████████████████████████████████████████████████████████
                   🏗️ CRIAR NOVO TESTE (Template)
█████████████████████████████████████████████████████████████████████████████████████

# Se quer testar validação de um novo campo no schema:

def test_novo_campo_valido(self, schema):
    \"\"\"
    CENÁRIO: Novo campo tem valor válido
    ESPERADO: Schema aceita
    \"\"\"
    data = {..., 'novo_campo': 'valor_valido'}
    result = schema.load(data)
    assert 'novo_campo' in result


# Se quer testar uma rota:

def test_nova_rota(self, client, clean_db, auth_headers):
    \"\"\"
    CENÁRIO: Usuario acessa nova rota com JWT
    ESPERADO: Retorna 200
    \"\"\"
    response = client.post(
        '/api/novo/endpoint',
        json={'data': 'value'},
        headers=auth_headers
    )
    assert response.status_code == 200


# Depois execute:
pytest seu_arquivo.py::test_novo_teste -v


█████████████████████████████████████████████████████████████████████████████████████
                     ❓ PRECISA DE AJUDA?
█████████████████████████████████████████████████████████████████████████████████████

Se um teste falhar:

1. Leia a mensagem de erro com atenção
2. Execute com -vv: pytest arquivo.py::teste -vv
3. Procure no TUTORIAL_TESTES.py por conceito similar
4. Veja outros testes como exemplo
5. Use: pytest arquivo.py::teste -s para ver prints


Comandos de apoio:
  pytest --version              # Ver versão
  pytest --help                 # Ver todas as opções
  pytest --markers              # Ver marcadores disponívés


█████████████████████████████████████████████████████████████████████████████████████
                         ✔️ PRÓXIMOS PASSOS
█████████████████████████████████████████████████████████████████████████████████████

Agora que você tem toda a estrutura:

☐ Execute: pytest tests/ -v
☐ Leia: TUTORIAL_TESTES.py
☐ Adicione testes para suas próprias features
☐ Execute cobertura: pytest --cov
☐ Compartilhe os testes com seu time

Parabéns! 🎉 Você tem testes profissionais agora!

""")

