# Documentação de Testes - Cadastro de Transação

---
## 1. Identificação

| Campo | Valor |
|---|---|
| **Feature** | Cadastro de Transação |
| **Cenário** | CEN-01 |
| **Requisito(s)** | R07 |
| **Branch de desenvolvimento** | `feature/6-cadastro-transacao` |
| **Branch de teste** | `test/feature/6-cadastro-transacao` |
| **Sprint(s)** | 6 |
| **Responsáveis** | Daniel Filipe / Matheus Moretti |
| **Data** | 02/06/2026 |

---
## 2. Critérios de aceitação testáveis

> Acordados com a dupla de desenvolvimento no início da feature (issue #17).

- [x] Gestor consegue registrar transação com valor, data, tipo e descrição - `TS-01`, `TS-17`, `TS-22`
- [x] Categoria é obrigatória e listada a partir das categorias da empresa - `TS-06`, `TS-07`, `TS-26`
- [x] Valor deve ser positivo - `TS-03`, `TS-04`, `TS-23`
- [x] Data não pode ser futura - `TS-05`, `TS-24`
- [ ] Transação registrada aparece imediatamente no histórico - `TS-08`: bloqueado pelo **DEF-01** (bug `Decimal - float` herdado da feature 7)
- [x] Gestor consegue editar uma transação existente - `TS-09` (+ `TS-10`, `TS-11`), `TS-21`
- [x] Gestor consegue excluir uma transação - `TS-12` (+ `TS-13`, `TS-14`)
- [ ] (implícito) Operação restrita à empresa do usuário autenticado - `TS-15`: o vínculo `user_company` não é checado → **DEF-02**

> **Rastreabilidade do roteiro:** `TS-05` (validação de valor/data/categoria) → casos `TS-03/04/05/06` + unit `TS-16` + front `TS-23/24/25`; `TS-16` (cadastro vinculado à categoria via API) → casos `TS-01/07`; `TS-24` (formulário de cadastro no front) → casos `TS-20`-`TS-27`.

---
## 3. Casos executados

| Caso  | Descrição                                            | Nível            | Esperado                            | Observado                           | Status |
|:-----:|------------------------------------------------------|------------------|-------------------------------------|-------------------------------------|:------:|
| TS-01 | `POST /api/transactions/` com dados válidos          | Integração       | `201` + `transaction_id`            | Conforme                            |   OK   |
| TS-02 | `POST` sem token                                     | Integração       | `401`                               | Conforme                            |   OK   |
| TS-03 | `POST` com valor negativo                            | Integração       | `400` (validação)                   | Conforme                            |   OK   |
| TS-04 | `POST` com valor zero                                | Integração       | `400` (valor estritamente positivo) | Conforme                            |   OK   |
| TS-05 | `POST` com data futura                               | Integração       | `400` (data não futura)             | Conforme                            |   OK   |
| TS-06 | `POST` sem categoria                                 | Integração       | `400` (categoria obrigatória)       | Conforme                            |   OK   |
| TS-07 | `POST` com categoria de outra empresa                | Integração       | `400` (não pertence à empresa)      | Conforme                            |   OK   |
| TS-08 | Transação recém-criada aparece no histórico          | Integração       | `200` + transação listada           | `500` `Decimal - float` (DEF-01)    | xfail  |
| TS-09 | `PUT` edita transação existente                      | Integração       | `200` + persistência confirmada     | Conforme (relido do banco)          |   OK   |
| TS-10 | `PUT` em transação inexistente                       | Integração       | `404`                               | Conforme                            |   OK   |
| TS-11 | `PUT` sem `company_id` no corpo                      | Integração       | `400`                               | Conforme                            |   OK   |
| TS-12 | `DELETE` exclui transação                            | Integração       | `200` + sai do histórico            | Conforme                            |   OK   |
| TS-13 | `DELETE` em transação inexistente                    | Integração       | `404`                               | Conforme                            |   OK   |
| TS-14 | `DELETE` sem `company_id`                            | Integração       | `400`                               | Conforme                            |   OK   |
| TS-15 | Usuário sem vínculo cria transação em empresa alheia | Integração       | `403`                               | `201` - `user_id` ignorado (DEF-02) | xfail  |
| TS-16 | `create_transaction` com categoria inexistente       | Unitário         | `400`                               | Conforme                            |   OK   |
| TS-17 | `create_transaction` com dados válidos               | Unitário         | `201` + `add`/`commit`              | Conforme                            |   OK   |
| TS-18 | `update_transaction` em transação inexistente        | Unitário         | `404`                               | Conforme                            |   OK   |
| TS-19 | `delete_transaction` em transação inexistente        | Unitário         | `404`                               | Conforme                            |   OK   |
| TS-20 | Modal exibe título "Nova Transação"                  | Unitário (front) | título de criação                   | Conforme                            |   OK   |
| TS-21 | Modal exibe título "Editar Transação" ao editar      | Unitário (front) | título de edição                    | Conforme                            |   OK   |
| TS-22 | Submeter formulário válido chama `onSalvar`          | Unitário (front) | `valor`/`categoriaId` numéricos     | Conforme                            |   OK   |
| TS-23 | Valor negativo bloqueia envio                        | Unitário (front) | erro + `onSalvar` não chamado       | Conforme                            |   OK   |
| TS-24 | Data futura bloqueia envio                           | Unitário (front) | erro + `onSalvar` não chamado       | Conforme                            |   OK   |
| TS-25 | Categoria obrigatória bloqueia envio                 | Unitário (front) | erro + `onSalvar` não chamado       | Conforme                            |   OK   |
| TS-26 | Select de categoria filtra pelo tipo selecionado     | Unitário (front) | só categorias do tipo               | Conforme                            |   OK   |
| TS-27 | Botão Cancelar chama `onFechar`                      | Unitário (front) | `onFechar` chamado                  | Conforme                            |   OK   |

---
## 4. Evidências

> Os resultados batem com os artifacts da pipeline (GitHub Actions, workflow `tests.yml`):
> `testes/relatorio-backend/test-results.xml` e `coverage.xml` já incluem
> `tests.unit.feature_6` e `tests.integration.feature_6` (17 pass, 0 fail, 2 xfail).

### Backend - `python -m pytest tests/unit/feature_6 tests/integration/feature_6 -q`

```
tests/unit/feature_6/test_transaction_service.py ....
tests/integration/feature_6/test_transaction_crud.py .......x......x....

================== 17 passed, 2 xfailed in 8.67s ==================
```

Os 2 `xfail`:
```
TS-08  test_transacao_aparece_no_historico                          -> DEF-01
TS-15  test_usuario_sem_vinculo_cria_transacao_em_empresa_alheia    -> DEF-02
```

### Frontend - `npm run test:run -- src/pages/Transacoes/ModalTransacao.test.jsx`

```
 src/pages/Transacoes/ModalTransacao.test.jsx (8 tests)
 Test Files  1 passed (1)
      Tests  8 passed (8)
```

**Total:** 27 testes - **25 passaram**, **2 xfail** (defeitos documentados), 0 falha inesperada.

---
## 5. Defeitos encontrados

> Os defeitos eram **esperados** nesta entrega e **não reprovam** a feature (ver §7).
> Estão alinhados às issues de correção/refatoração já abertas: **#54** (Fix II -
> diferenciação contas/transações e correções do histórico), **#56** (Fix III -
> integração entre classes) e **#35** (Tarefa V - refatoração).

| Issue          | Descrição                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Status |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| DEF-01 (→ #54) | `get_history_filtered` (`transaction_service.py:39`) estoura `TypeError: unsupported operand type(s) for -: 'decimal.Decimal' and 'float'` quando o histórico tem **só um tipo** de transação (`receitas`/`despesas` vazio vira `0.0` float vs `Decimal`). Como uma transação recém-criada costuma ser o único registro, **não foi possível confirmar "aparece imediatamente no histórico"** via API (HTTP 500). Bug pré-existente, herdado da feature 7 (não é regressão da feature 6). Branch sugerida: `fix/historico-totais-decimal`. | Aberto |
| DEF-02 (→ #56) | `create_transaction` valida que a categoria pertence ao `company_id` informado, mas **não verifica se o usuário autenticado está vinculado à empresa** (`user_id` é apenas carimbado). Um usuário sem vínculo registra transação em empresa alheia (deveria `403`). Espelha o DEF-03 da feature 5. **Impacto de autorização.** Branch sugerida: `fix/transacao-autorizacao-empresa`.                                                                                                                                                      | Aberto |
| DEF-03 (→ #35) | `app/repositories/transaction_repository.py` é **código morto** (cobertura 0%, nunca importado); o service consulta os models diretamente. Candidato à refatoração. Branch sugerida: `refactor/transacao-usa-repository`.                                                                                                                                                                                                                                                                                                                 | Aberto |

---
## 6. Cobertura

```bash
# Backend
pytest tests/unit/feature_6 tests/integration/feature_6 \
  --cov=app.services.transaction_service --cov=app.routes.transaction_routes \
  --cov=app.schemas.transaction_schema --cov=app.models.transaction \
  --cov=app.repositories.transaction_repository --cov-report=term-missing

# Frontend
npm run test:run -- src/pages/Transacoes/ModalTransacao.test.jsx --coverage
```

| Métrica                                           | Valor                                                                                |
|---------------------------------------------------|--------------------------------------------------------------------------------------|
| `app/schemas/transaction_schema.py`               | 100%                                                                                 |
| `app/models/transaction.py`                       | 95%                                                                                  |
| `app/routes/transaction_routes.py`                | 89%                                                                                  |
| `app/services/transaction_service.py`             | 69% (o não-coberto é `get_history_filtered` - escopo da feature 7 - e ramos de erro) |
| `app/repositories/transaction_repository.py`      | 0% (código morto - ver DEF-03)                                                       |
| **Backend - total (módulos importados)**          | **83%**                                                                              |
| `src/pages/Transacoes/ModalTransacao.jsx` (front) | núcleo do formulário coberto pelos 8 testes                                          |

Núcleo do cadastro (criar/editar/excluir + validações) acima da meta de **≥ 60%**.

---
## 7. Parecer final

> **Status:** Aprovada com pendências.
>
> O cadastro de transação está coberto e verde (**25/27**, cobertura **83%** no
> backend e formulário do front exercitado). Criar, editar e excluir funcionam; as
> validações de **valor positivo**, **data não futura**, **categoria obrigatória** e
> **categoria pertencente à empresa** são respeitadas tanto no schema do backend
> quanto na validação client-side do `ModalTransacao`.
>
> Os defeitos **DEF-01/02** e a pendência de refatoração **DEF-03** eram **esperados**
> e **não impedem a aprovação** - estão documentados como `xfail` e endereçados pelas
> issues já abertas (#54, #56, #35). O critério "aparece imediatamente no histórico"
> fica **pendente** até a correção do DEF-01.
>
> **Próximos passos (não bloqueantes):**
> 1. **DEF-01** - normalizar `Decimal`/`float` em `get_history_filtered` (corrige também a feature 7); depois `TS-08` deve ficar verde.
> 2. **DEF-02** - validar o vínculo `user_company` a partir do `user_id` do JWT *(autorização)*.
> 3. **DEF-03** - usar o `transaction_repository` (hoje código morto) ou removê-lo (refatoração #35).

---
