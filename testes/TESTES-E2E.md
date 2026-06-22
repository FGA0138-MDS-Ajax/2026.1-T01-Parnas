# Testes E2E (End-to-End) — Backend

> Guia para testes **E2E** (de ponta a ponta). Pré-requisito: o ambiente e as
> fixtures de **TESTES-BACK.md**. Hoje fazemos **E2E de API**; o E2E de navegador
> (Playwright) ainda será configurado — ver seção 6.

---

## 1. Teoria: o que é um teste E2E?

E2E significa **end-to-end** — "de uma ponta à outra". Em vez de testar uma rota
isolada (integração) ou uma função (unitário), o E2E simula uma **jornada
completa do usuário**, encadeando **vários passos em sequência**, onde o resultado
de um passo alimenta o próximo.

Exemplo de jornada:

```
registrar usuário  →  fazer login (pegar o token)  →  usar o token para cadastrar
empresa  →  conferir que a empresa aparece ao consultar
```

Cada seta é um endpoint diferente, e o token obtido no login é **reutilizado** nos
passos seguintes. É o teste mais próximo do uso real — e por isso o mais lento e o
que existe em **menor quantidade** (topo da pirâmide).

**Integração responde:** "esse endpoint funciona?"
**E2E responde:** "o usuário consegue ir do início ao fim da tarefa dele?"

---

## 2. Onde escrever

- **Onde:** `backend/tests/e2e/`
- **Arquivo:** `test_<fluxo>.py` (ex.: `test_fluxo_cadastro_login.py`)

Usa as fixtures do `conftest.py` — principalmente `client` e `clean_db`. Note que
no E2E muitas vezes **criamos o usuário e o token dentro do próprio teste** (faz
parte da jornada), em vez de usar `auth_headers` pronto.

---

## 3. Exemplos

### Exemplo 1 — jornada cadastro → login → cadastrar empresa

```python
# backend/tests/e2e/test_fluxo_cadastro_login.py
def test_fluxo_cadastro_login_e_empresa(client, clean_db):
    # 1) Registrar usuário
    client.post('/api/register', json={
        'name': 'Maria', 'email': 'maria@email.com',
        'password': 'Senha@123', 'cpf': '12345678901',
        'birth_date': '2000-01-01',
    })

    # 2) Login → obtém o token (passo que alimenta os próximos)
    login = client.post('/auth/login', json={
        'email': 'maria@email.com', 'password': 'Senha@123',
    })
    token = login.get_json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # 3) Com o token, cadastra a empresa
    resp = client.post('/api/companies/register', json={
        'name': 'Padaria da Maria', 'cnpj': '11.222.333/0001-81',
        'email': 'padaria@email.com', 'phone': '1130000000',
    }, headers=headers)

    # Assert final da jornada
    assert resp.status_code == 201
```

### Exemplo 2 — login inválido interrompe o fluxo

```python
def test_login_invalido_nao_da_acesso(client, clean_db):
    # Sem registrar ninguém, tenta logar
    login = client.post('/auth/login', json={
        'email': 'ninguem@email.com', 'password': 'errada',
    })

    # A jornada para aqui: sem token, sem acesso
    assert login.status_code == 401
    assert 'access_token' not in login.get_json()
```

---

## 4. Como rodar

```bash
pytest tests/e2e/                              # todos os fluxos E2E
pytest tests/e2e/test_fluxo_cadastro_login.py
pytest --cov=app tests/e2e/                    # com cobertura
```

---

## 5. Checklist antes de dar o teste por pronto

- [ ] Arquivo em `tests/e2e/`, nome `test_*.py`.
- [ ] Encadeia **vários passos**, reaproveitando o resultado de um no próximo.
- [ ] Usa `clean_db` para a jornada começar do zero.
- [ ] O `assert` final reflete o **objetivo da jornada**, não só um passo.
- [ ] Se aplicável, mapeado ao roteiro (TS-13 e TS-14 são E2E).

---

## 6. E2E de navegador (Playwright) — ainda a configurar

O que está acima é **E2E de API**: testamos a jornada pelos endpoints, sem abrir
navegador. O projeto também prevê **E2E de navegador de verdade** com
**Playwright**, cobrindo os cenários **CEN-01 a CEN-04** (clicar na tela, preencher
formulários reais no Chrome/Firefox).

Isso **ainda não está montado**. Quando formos configurar, será em uma pasta
própria (provavelmente `frontend/e2e/` ou `e2e/` na raiz) com o Playwright
instalado à parte — e este guia será atualizado com o passo a passo. Por ora,
nosso E2E é o de API descrito acima.
