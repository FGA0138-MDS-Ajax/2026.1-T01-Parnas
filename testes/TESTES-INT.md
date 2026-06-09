# Testes de Integração — Backend

> Guia para testes de **integração** do backend. Pré-requisito: o ambiente e as
> fixtures descritos em **TESTES-BACK.md** (mesma `.venv`, mesmo `conftest.py`).

---

## 1. Teoria: o que é um teste de integração?

Enquanto o teste **unitário** isola uma função e mocka tudo ao redor, o teste de
**integração** faz o contrário: deixa as **peças reais conversarem entre si** e
verifica se elas se encaixam.

No nosso backend, uma requisição passa por várias camadas:

```
HTTP → rota (route) → service (regra de negócio) → repository → ORM → banco
```

O teste de integração chama o **endpoint de verdade** e deixa essa cadeia toda
rodar. A única coisa "de mentira" é o banco: usamos **SQLite em memória** — um
banco real, porém rápido e descartável, criado do zero a cada teste. **Não há
mock de banco aqui.** Se a rota, o service e o ORM não combinarem, o teste falha —
e é exatamente isso que queremos pegar.

**Unitário responde:** "essa função, sozinha, está correta?"
**Integração responde:** "essas peças, juntas, funcionam de ponta a ponta na rota?"

---

## 2. Onde escrever

- **Onde:** `backend/tests/integration/`
- **Arquivo:** `test_<recurso>.py` (ex.: `test_company_endpoints.py`)

Os testes usam as **fixtures do `conftest.py`** (ver TESTES-BACK.md):

| Fixture usada  | Para quê                                                          |
|----------------|-------------------------------------------------------------------|
| `client`       | fazer as requisições HTTP (`client.post(...)`, `client.get(...)`) |
| `clean_db`     | garantir um banco zerado antes/depois do teste                    |
| `auth_headers` | enviar requisições autenticadas (já com o JWT)                    |

---

## 3. Exemplos

### Exemplo 1 — cadastrar empresa (rota autenticada, feliz)

```python
# backend/tests/integration/test_company_endpoints.py
def test_cadastra_empresa_com_sucesso(client, auth_headers, clean_db):
    # Act: chama o endpoint REAL, autenticado
    resp = client.post(
        '/api/companies/register',
        json={
            'name': 'Padaria X',
            'cnpj': '11.222.333/0001-81',
            'email': 'contato@padariax.com',
            'phone': '1130000000',
        },
        headers=auth_headers,
    )

    # Assert: criou (201) e devolveu o nome
    assert resp.status_code == 201
    assert resp.get_json()['name'] == 'Padaria X'
```

### Exemplo 2 — verificando uma regra de negócio (CNPJ duplicado)

```python
def test_cnpj_duplicado_retorna_409(client, auth_headers, clean_db):
    payload = {
        'name': 'Padaria X',
        'cnpj': '11.222.333/0001-81',
        'email': 'contato@padariax.com',
        'phone': '1130000000',
    }
    # Arrange: cadastra a primeira vez
    client.post('/api/companies/register', json=payload, headers=auth_headers)

    # Act: tenta cadastrar de novo com o mesmo CNPJ
    resp = client.post('/api/companies/register', json=payload, headers=auth_headers)

    # Assert: o banco real + a regra do service barram com 409
    assert resp.status_code == 409
```

> Repare: aqui **não mockamos nada**. A validação de duplicidade só "prova" que
> funciona porque o primeiro cadastro foi mesmo gravado no banco em memória.

---

## 4. Como rodar

```bash
pytest tests/integration/                         # todos os de integração
pytest tests/integration/test_company_endpoints.py
pytest tests/integration/ -k cnpj                 # filtra por nome
pytest --cov=app tests/integration/               # com cobertura
```

---

## 5. Checklist antes de dar o teste por pronto

- [ ] Arquivo em `tests/integration/`, nome `test_*.py`.
- [ ] Usa `client` para chamar a **rota real** (nada de chamar o service direto).
- [ ] Usa `clean_db` para começar com o banco limpo.
- [ ] Rotas autenticadas recebem `auth_headers`.
- [ ] **Não mocka o banco** — o ponto do teste é justamente integrar com ele.
- [ ] Verifica o `status_code` **e** o conteúdo relevante da resposta.
- [ ] Se aplicável, mapeado ao roteiro (TS-06 a TS-12 são de integração).
