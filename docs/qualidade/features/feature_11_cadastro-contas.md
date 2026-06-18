# Documentação de Testes — Cadastro de Contas

---
## 1. Identificação

| Campo | Valor |
|---|---|
| **Feature** | Cadastro de Contas a Pagar e a Receber (US11) |
| **Cenário** | CEN-01 — Registro de dados financeiros |
| **Requisito(s)** | R15 |
| **Branch de desenvolvimento** | `feature/11-cadastro-contas` |
| **Branch de teste (QA)** | `test/feature/11-cadastro-contas` (a partir da `develop`) |
| **PR / Pipeline** | GitHub Actions `tests` (run 27772038130) — **success** |
| **Sprint(s)** | 7 |
| **Responsáveis** | Daniel Filipe / Matheus Moretti |
| **Data** | 18/06/2026 |

> A branch de teste foi baseada na `develop` (que já contém o código de Contas idêntico ao
> da `feature/11`, além da infraestrutura de testes); a `feature/11-cadastro-contas` original
> estava 57 commits atrás da `develop` e sem `conftest`.

---
## 2. Critérios de aceitação testáveis

- [x] **CA-01** Cadastrar conta com descrição, valor, tipo, vencimento e categoria — `TS-02`, `TS-09`
- [x] **CA-02** Contas listadas separadas por pendentes e quitadas — `TS-13` (back, filtro por status), `TS-22` (front)
- [~] **CA-03** Quitar conta pendente com confirmação — confirmação na UI OK (`TS-24`); o **endpoint de quitar falha** → **DEF-01**
- [ ] **CA-04** Ao quitar, é gerada automaticamente a transação correspondente — **quebrado** → **DEF-01** (`TS-21`, xfail)
- [x] **CA-05** Contas quitadas não podem ser editadas nem excluídas — `TS-04`, `TS-06` (unit), `TS-18`, `TS-19` (integr.), `TS-23` (front)
- [x] **CA-06** Editar e excluir contas pendentes — `TS-14`, `TS-16`

---
## 3. Casos executados

| Caso | Descrição | Nível | Esperado | Observado | Status |
| :--: | --- | --- | --- | --- | :--: |
| TS-01 | `_get_company_id` retorna a empresa do usuário | Unitário | `company_id` do usuário | Conforme | ✅ |
| TS-02 | `create_bill` persiste e retorna id | Unitário | `201` + `id`; `add`/`commit` chamados | Conforme | ✅ |
| TS-03 | `update_bill` em conta inexistente | Unitário | `404` | Conforme | ✅ |
| TS-04 | `update_bill` em conta quitada | Unitário | `400`, sem `commit` | Conforme | ✅ |
| TS-05 | `delete_bill` em conta inexistente | Unitário | `404` | Conforme | ✅ |
| TS-06 | `delete_bill` em conta quitada | Unitário | `400`, sem `delete` | Conforme | ✅ |
| TS-07 | `pay_bill` em conta inexistente | Unitário | `404` | Conforme | ✅ |
| TS-08 | `pay_bill` em conta já quitada | Unitário | `400` | Conforme | ✅ |
| TS-09 | `POST /api/contas` com dados válidos | Integração | `201` + `id` | Conforme | ✅ |
| TS-10 | `POST /api/contas` com campo obrigatório faltando | Integração | `400` | Conforme | ✅ |
| TS-11 | `POST /api/contas` sem token | Integração | `401` | Conforme | ✅ |
| TS-12 | `GET /api/contas` lista as contas da empresa | Integração | `200` + 2 contas | Conforme | ✅ |
| TS-13 | `GET /api/contas?status=` filtra pendentes/quitadas | Integração | só as do status pedido | Conforme | ✅ |
| TS-14 | `PUT /api/contas/<id>` edita conta pendente | Integração | `200` | Conforme | ✅ |
| TS-15 | `PUT /api/contas/<id>` em conta inexistente | Integração | `404` | Conforme | ✅ |
| TS-16 | `DELETE /api/contas/<id>` exclui conta pendente | Integração | `200` + some da lista | Conforme | ✅ |
| TS-17 | `DELETE /api/contas/<id>` em conta inexistente | Integração | `404` | Conforme | ✅ |
| TS-18 | `PUT /api/contas/<id>` em conta quitada | Integração | `400` (bloqueado) | Conforme | ✅ |
| TS-19 | `DELETE /api/contas/<id>` em conta quitada | Integração | `400` (bloqueado) | Conforme | ✅ |
| TS-20 | `PATCH /api/contas/<id>/quitar` em conta já quitada | Integração | `400` | Conforme | ✅ |
| TS-21 | `PATCH /api/contas/<id>/quitar` em conta pendente gera transação | Integração | `200` + transação criada | `IntegrityError` (`transaction.type` NOT NULL) | ⏭️ xfail (DEF-01) |
| TS-22 | Lista contas separadas em Pendentes e Quitadas | Unitário (front) | duas seções com as contas | Conforme | ✅ |
| TS-23 | Conta quitada não exibe ações (quitar/editar/excluir) | Unitário (front) | só selo "✓ Quitada" | Conforme | ✅ |
| TS-24 | Quitar pendente pede confirmação e chama o serviço | Unitário (front) | modal + `liquidarConta(id)` | Conforme | ✅ |
| TS-25 | Excluir pendente: "Cancelar" não chama o serviço | Unitário (front) | `removerConta` não chamado | Conforme | ✅ |

> Os casos de front (`TS-22`…`TS-25`) são testes de componente (Vitest) com o hook
> `useContas` mockado. **Observação de integração:** a página de Contas ainda consome
> dados de `CONTAS_MOCK` e o `conta.service.js` está vazio — o front **não está plugado
> à API** (tema da issue #54, em andamento). Por isso não há cobertura end-to-end.

---
## 4. Evidências

Execução pela **pipeline** (GitHub Actions, workflow `tests`, run `27772038130`),
artefatos em `testes/relatorio-backend/` e `testes/relatorio-frontend/`.

### Backend — `pytest`

```
tests/unit/feature_11/test_bill_service.py ........            (8 passed)
tests/integration/feature_11/test_bill_endpoints.py ............x  (12 passed, 1 xfail)
...
===== 6 failed, 188 passed, 14 xfailed, 1 xpassed, 298 warnings in 40.92s ======
```

- **Os 21 testes da feature passaram** (20 verde + 1 xfail documentando o **DEF-01**).
- As **6 falhas** são **pré-existentes e fora do escopo** — todas em `feature_6`
  (transações): assinaturas divergentes (`current_user_id` / `company_id`) e
  `ProgrammingError: type 'dict' is not supported`. Pertencem ao relatório da feature 6.

### Frontend — `vitest run --coverage`

```
✓ src/pages/Contas/Contas.test.jsx (4 tests) 562ms
 Test Files  9 passed (9)
      Tests  53 passed | 3 skipped (56)
```

---
## 5. Defeitos encontrados

| Issue | Descrição | Branch de correção | Status |
|---|---|---|---|
| DEF-01 | `BillService.pay_bill` cria a `Transaction` de quitação **sem o campo `type`**, mas `Transaction.type` é `NOT NULL` → `IntegrityError: NOT NULL constraint failed: transaction.type`. O endpoint `PATCH /api/contas/<id>/quitar` falha e **não gera a transação** (CA-03/CA-04). | `fix/contas-quitar-type-transacao` | Aberto |
| DEF-02 | Front de Contas **não integrado à API**: usa `CONTAS_MOCK` e `conta.service.js` está vazio. Sem persistência real (criar/listar/editar/excluir/quitar não chamam o backend). Em andamento na issue #54. | `fix/contas-integra-api` | Aberto |
| DEF-03 | Divergência no valor de `type`: o model `Bill` documenta `'pagar'`/`'receber'`, enquanto o front usa `'receita'`/`'despesa'`. Pode causar inconsistência ao integrar. (menor) | `fix/contas-padroniza-tipo` | Aberto |

---
## 6. Cobertura

### Backend — `coverage.xml` (artefato da pipeline)

| Módulo | Cobertura (linhas) |
|---|---|
| `app/routes/bill_routes.py` | **100%** |
| `app/services/bill_service.py` | **96,9%** |
| `app/models/bill.py` | **94,7%** |
| `app/repositories/bill_repository.py` | **0%** (código morto — o service não usa o repository) |

### Frontend — `coverage/` (artefato da pipeline)

| Módulo | Cobertura (linhas) | Observação |
|---|---|---|
| `src/pages/Contas/Contas.jsx` | **89,5%** | exercitado por `TS-22`…`TS-25` |
| `src/pages/Contas/Modalconta.jsx` | **2,4%** | formulário do modal de nova/editar conta — sem teste dedicado |
| `src/pages/Contas/Usecontas.jsx` | **0%** | hook mockado nos testes de componente |
| `src/pages/Contas/` (pasta) | **44,0%** | puxada para baixo pelo `Modalconta` e `Usecontas` |

O núcleo do backend fica bem acima da meta de **≥ 60%**; no front, o componente principal
(`Contas.jsx`) também, mas o hook (não integrado) e o modal derrubam a média da pasta.

---
## 7. Parecer final

> **Status:** 🚧 **Aprovada com pendências**
>
> O **CRUD de contas e as regras de negócio do backend estão sólidos e verdes**: criar,
> listar, filtrar por status, editar e excluir, além dos bloqueios de edição/exclusão de
> conta quitada e das validações (400/401/404) — 20 testes passando com cobertura de
> 95–100% nos módulos relevantes. No front, o componente `Contas.jsx` cobre a separação
> pendentes/quitadas, a ausência de ações em contas quitadas e os fluxos de confirmação
> (quitar/excluir).
>
> **Pendências registradas:**
> 1. **DEF-01 (prioritário)** — o `pay_bill` quebra ao quitar (`Transaction` sem `type`,
>    que é `NOT NULL`); a quitação e a geração automática de transação (CA-03/CA-04) não
>    funcionam. Correção provável de 1 linha: definir o `type` da transação (a partir da
>    categoria) ao criar a transação de quitação.
> 2. **DEF-02** — integrar o front à API (hoje em `CONTAS_MOCK`; `conta.service.js` vazio).
> 3. **DEF-03** — padronizar o valor de `type` entre model e front.
>
> Recomenda-se priorizar o **DEF-01** (defeito funcional de backend) antes de considerar a
> feature concluída.
