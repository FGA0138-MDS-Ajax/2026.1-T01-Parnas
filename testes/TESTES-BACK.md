# Testes do Backend — Unitários (e base para todos os outros)

> Este é o guia **base do backend**. Aqui está como montar o ambiente, como
> funcionam as *fixtures* compartilhadas e como escrever testes **unitários**.
> Integração e E2E reaproveitam tudo isto — então leia este primeiro.

---

## 1. Teoria: o que é um teste unitário?

Um teste **unitário** verifica a **menor unidade de lógica** do sistema — uma
função ou um método — **isolada de tudo o mais**. "Isolada" quer dizer: **sem
banco de dados e sem rede**. Se a função que estamos testando depende de algo
externo (o banco, outro service, o relógio do sistema), nós **substituímos essa
dependência por um *mock*** — um objeto falso que finge ser a coisa real e
responde do jeito que mandamos.

Por que isolar? Porque assim o teste:
- é **rápido** (não espera banco nem rede);
- é **confiável** (não quebra por causa de um banco fora do ar);
- aponta o **culpado certo** (se falhou, o problema está *naquela* função, não em
  outra peça).

### O padrão AAA

Todo teste segue três passos, nesta ordem:

1. **Arrange** (Arrumar) — prepara os dados e os mocks.
2. **Act** (Agir) — chama a função que está sendo testada.
3. **Assert** (Afirmar) — verifica se o resultado é o esperado.

---

## 2. Montando o ambiente

A partir da pasta `backend/`:

```bash
python -m venv .venv          # cria o ambiente virtual
source .venv/bin/activate     # ativa (Linux/macOS)
# .venv\Scripts\activate      # ativa (Windows)
pip install -r requirements.txt
```

As ferramentas de teste já estão no `requirements.txt`:

| Pacote        | Para quê                               |
|---------------|----------------------------------------|
| `pytest`      | o executor de testes                   |
| `pytest-mock` | dá a fixture `mocker` para criar mocks |
| `pytest-cov`  | mede a cobertura de testes             |

### O `pytest.ini`

```ini
[pytest]
testpaths = tests          # só procura testes dentro de tests/
python_files = test_*.py   # arquivos de teste começam com test_
python_classes = Test*     # classes de teste começam com Test
python_functions = test_*  # funções de teste começam com test_
addopts = -v               # saída detalhada
```

> **Importante:** como `testpaths = tests`, qualquer `test_*.py` solto dentro de
> `app/` é **ignorado**. Todo teste do back mora em `tests/unit`, `tests/integration`
> ou `tests/e2e` (todas são pacotes Python, têm `__init__.py`).

---

## 3. As fixtures compartilhadas (`tests/conftest.py`)

O pytest carrega o `conftest.py` automaticamente. Tudo que está lá vira uma
**fixture** disponível em *qualquer* teste do backend — basta pedir pelo nome
como argumento da função de teste. As principais:

| Fixture        | O que entrega                                                |
|----------------|--------------------------------------------------------------|
| `app`          | a aplicação Flask configurada para teste (SQLite em memória) |
| `client`       | um cliente HTTP para chamar os endpoints sem subir servidor  |
| `app_context`  | contexto de app para mexer no banco fora de uma requisição   |
| `clean_db`     | zera o banco antes e depois do teste                         |
| `test_user`    | um usuário já salvo no banco (`teste@email.com`)             |
| `auth_token`   | um JWT válido desse usuário                                  |
| `auth_headers` | os headers HTTP já com o `Bearer <token>`                    |

> Unitários quase não usam essas fixtures (eles mockam tudo). Quem mais usa são os
> testes de **integração** e **E2E**. Mas elas moram aqui, na base do backend.

---

## 4. Escrevendo testes unitários

- **Onde:** `backend/tests/unit/`
- **Arquivo:** `test_<o-que-testa>.py` (ex.: `test_company_service.py`)
- **Função:** `def test_<comportamento>(...)`

### Regra de ouro do mock: mocke onde a dependência é **usada**

Se o `company_service.py` faz `from app.models.company import Company` e usa
`Company`, você mocka `app.services.company_service.Company` (onde ele é *usado*),
**não** `app.models.company.Company` (onde foi *definido*). Esse é o erro nº 1 de
quem começa.

### Exemplo 1 — testando um validador puro

```python
# backend/tests/unit/test_validators.py
from app.utils.validators import is_valid_email

def test_email_valido_retorna_true():
    # Act + Assert (função pura, nada a "arranjar")
    assert is_valid_email('joao@email.com') is True

def test_email_sem_arroba_retorna_false():
    assert is_valid_email('joao.email.com') is False
```

### Exemplo 2 — testando um service com mock (sem tocar o banco)

```python
# backend/tests/unit/test_company_service.py
from app.services.company_service import register_company

def test_cnpj_duplicado_retorna_409(mocker):
    # Arrange: finge que JÁ existe uma empresa com esse CNPJ.
    # Mockamos Company onde ele é USADO (no módulo do service).
    mock_company = mocker.patch('app.services.company_service.Company')
    mock_company.query.filter_by.return_value.first.return_value = object()

    # Act: chama a função real do service
    body, status = register_company(
        user_id=1,
        data={'cnpj': '11.222.333/0001-81'},
    )

    # Assert: deve barrar com 409 (conflito)
    assert status == 409
```

---

## 5. Como rodar

```bash
pytest                       # tudo (unit + integration + e2e)
pytest tests/unit/           # só os unitários
pytest tests/unit/test_company_service.py   # um arquivo
pytest -k cnpj               # só testes cujo nome contém "cnpj"
pytest -v                    # saída detalhada (já é o padrão pelo addopts)
pytest --cov=app tests/      # com cobertura (meta: ≥ 60% até a Sprint 5)
```

---

## 6. Checklist antes de dar o teste por pronto

- [ ] O arquivo está em `tests/unit/` e começa com `test_`.
- [ ] O teste **não toca banco nem rede** (se toca, é integração — outro guia).
- [ ] Dependências externas estão **mockadas onde são usadas**.
- [ ] Segue **AAA** e tem nome que descreve o comportamento.
- [ ] Cobre **um** comportamento por teste.
- [ ] Se aplicável, está mapeado a um caso do roteiro (TS-01…TS-05 são unitários).
