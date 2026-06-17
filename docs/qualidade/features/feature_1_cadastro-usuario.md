# Documentação de Testes — Cadastro de Usuário

---
## 1. Identificação

| Campo                         | Valor                             |
|-------------------------------|-----------------------------------|
| **Feature**                   | Cadastro de usuário               |
| **Cenário**                   | CEN-00                            |
| **Requisito(s)**              | R01                               |
| **Branch de desenvolvimento** | `feature/1-cadastro-usuario`      |
| **Branch de teste**           | `test/feature/1-cadastro-usuario` |
| **Sprint(s)**                 | 4                                 |
| **Responsáveis**              | Daniel Filipe / Matheus Moretti   |
| **Data**                      | 22/05/2026                        |

---
## 2. Critérios de aceitação testáveis

- [x] E-mail já cadastrado é barrado (HTTP 409).
- [x] CPF já cadastrado é barrado (HTTP 409).
- [x] Cadastro válido cria a conta e retorna token (HTTP 201).
- [x] Falha interna ao salvar faz rollback e retorna HTTP 500.
- [x] Senha exige ≥ 8 caracteres, com letra, número e caractere especial.
- [ ] Senha não pode conter espaços. *(falhando — ver DEF-01)*
- [x] Data de nascimento inválida/futura/idade insuficiente é rejeitada.
- [x] A tela de cadastro valida data futura e idade mínima antes de enviar.
- [ ] Cadastro pela tela envia os dados ao backend com sucesso. *(bloqueado — ver DEF-02)*

---
## 3. Casos executados

| Caso  | Descrição                                                   | Nível    | Esperado                           | Observado             | Status |
|:-----:|-------------------------------------------------------------|----------|------------------------------------|-----------------------|:------:|
| TS-01 | `register_user` com e-mail duplicado                        | Unitário | `{erro: ...}`, 409                 | Conforme              |   ✅    |
| TS-02 | `register_user` com CPF duplicado                           | Unitário | `{erro: ...}`, 409                 | Conforme              |   ✅    |
| TS-03 | `register_user` com dados válidos                           | Unitário | mensagem + token, 201              | Conforme              |   ✅    |
| TS-04 | `register_user` com erro no commit                          | Unitário | rollback + 500                     | Conforme              |   ✅    |
| TS-05 | `is_valid_password` — vazio/curta/sem letra/número/especial | Unitário | `False`                            | Conforme              |   ✅    |
| TS-06 | `is_valid_password` — senha válida                          | Unitário | `True`                             | Conforme              |   ✅    |
| TS-07 | `is_valid_password` — senha com espaços                     | Unitário | `False`                            | Retorna `True`        |   ❌    |
| TS-08 | `is_valid_birth_date` — data inválida/futura/idade/formato  | Unitário | `False`                            | Conforme              |   ✅    |
| TS-09 | `is_valid_birth_date` — data válida                         | Unitário | `True`                             | Conforme              |   ✅    |
| TS-10 | UI cadastro — tela renderiza (título e botão)               | Unitário | Elementos na tela                  | Conforme              |   ✅    |
| TS-11 | UI cadastro — data de nascimento no futuro                  | Unitário | Erro "Data de nascimento inválida" | Conforme              |   ✅    |
| TS-12 | UI cadastro — menor de 18 anos                              | Unitário | Erro "pelo menos 18 anos"          | Conforme              |   ✅    |
| TS-13 | UI cadastro — adulto não acusa erro de data/idade           | Unitário | Sem erro de data/idade             | Conforme              |   ✅    |
| TS-14 | UI cadastro — envio válido chama `POST /auth/register`      | Unitário | `fetch` chamado                    | `fetch` não é chamado |   ⏭️   |

> TS-14 está marcado como `test.skip` no código por causa do DEF-02 (caminho feliz
> bloqueado). Reativar quando o defeito for corrigido.

---
## 4. Evidências

**Backend — `backend/`**
```bash
python -m pytest tests/unit/feature_1/ -v
```
```
30 passed, 2 failed in 0.06s
FAILED test_validators.py::test_is_valid_password_spaces[  1!JOAO         ]
FAILED test_validators.py::test_is_valid_password_spaces[Senha 67!]
```

**Frontend — `frontend/`**
```bash
npm run test:run
```
```
✓ src/pages/Register/Register.test.jsx (5 tests | 1 skipped)
Tests  4 passed | 1 skipped (5)
```

---
## 5. Defeitos encontrados

| Issue          | Descrição                                                                                                                                                                                                | Status  |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------| 
| #— *(a abrir)* | **DEF-01:** `is_valid_password` aceita senha com espaços; deveria rejeitar (`'Senha 67!'` retorna `True`).                                                                                               | Aberto  |
| #— *(a abrir)* | **DEF-02:** Em `Register.jsx`, os campos **Nome** e **Senha** não têm `value`/`onChange`; o estado nunca é preenchido, `senha` fica `""` e o cadastro trava em "senha < 8". Impede o cadastro pela tela. | Aberto  |
| #— *(a abrir)* | **DEF-03:** `Register.jsx` lê `data.message` na resposta de erro, mas o backend retorna a mensagem em `data.erro`; o usuário sempre vê o texto genérico.                                                 | Aberto  |

---
## 6. Cobertura

```bash
pytest tests/unit/feature_1/ --cov=app.services.user_service --cov=app.utils.validators
```

| Métrica                              | Valor |
|--------------------------------------|-------|
| `app/services/user_service.py`       | 100%  |
| `app/utils/validators.py`            | 100%  |
| Cobertura da feature (módulos acima) | 100%  |

> Frontend: a UnitTest do componente cobre as validações de data/idade e a
> renderização; o caminho feliz fica pendente até o DEF-02 ser corrigido.

---
## 7. Parecer final

**Status:** Aprovada com pendências

A lógica de cadastro do backend (`register_user`) e a validação de data de
nascimento estão cobertas (100%) e aprovadas. Ficam três pendências antes do
fechamento definitivo:

- **DEF-01** — validador de senha aceita espaços (2 testes vermelhos);
- **DEF-02** — bug que impede o cadastro pela tela (caminho feliz bloqueado, TS-14);
- **DEF-03** — mensagem de erro do backend não é exibida na UI.

