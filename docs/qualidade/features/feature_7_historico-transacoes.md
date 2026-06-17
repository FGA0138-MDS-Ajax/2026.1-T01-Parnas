# Documentação de Testes — Histórico de Transações

## 1. Identificação

| Campo                         | Valor                                 |
|-------------------------------|---------------------------------------|
| **Feature**                   | US07 — Histórico de Transações        |
| **Cenário**                   | CEN-01                                |
| **Requisito**                 | R08                                   |
| **Prioridade**                | Should                                |
| **Branch de desenvolvimento** | `feature/7-historico-transacoes`      |
| **Branch de teste (QA)**      | `test/feature/7-historico-transacoes` |
| **Sprint**                    | 6                                     |
| **Responsáveis (QA)**         | Daniel Filipe / Matheus Moretti       |
| **Data**                      | 06/06/2026                            |

## 2. Critérios de aceitação testáveis

- [x] Visualiza todas as transações da empresa em ordem cronológica — `TS-04`, `TS-24`
- [x] Filtrar por período (data início e data fim) — `TS-05`, `TS-17`
- [ ] Filtrar por tipo (receita/despesa) — `TS-15` (front) ✅, mas `TS-06` (back) **falha** → ver **DEF-01**
- [x] Filtrar por categoria — `TS-07`, `TS-16`
- [x] Filtrar por valor mínimo e máximo — `TS-08`, `TS-18`
- [ ] Total de receitas, despesas e saldo do período **filtrado** — `TS-09` (sem filtro) ✅, mas `TS-10` (totais com filtro que isola um tipo) **falha** → ver **DEF-01**
- [ ] Lista paginada (máximo 20 itens por página) — back pagina corretamente (`TS-11`, `TS-12`); front pagina a **5** itens, não 20 → ver **DEF-02**
- [x] Apenas transações da empresa autenticada são retornadas — `TS-01`, `TS-02`, `TS-03`

## 3. Casos executados

| Caso  | Descrição                                                        | Nível      | Esperado                                           | Observado                           | Status |
|-------|------------------------------------------------------------------|------------|----------------------------------------------------|-------------------------------------|--------|
| TS-01 | `GET /api/transactions/` sem `company_id`                        | Integração | `400` + "company_id é obrigatório"                 | Conforme                            | ✅      |
| TS-02 | `GET /api/transactions/` sem token                               | Integração | `401`                                              | Conforme                            | ✅      |
| TS-03 | Lista escopada por empresa/usuário (ignora ruído)                | Integração | só as 4 da empresa A do usuário                    | Conforme                            | ✅      |
| TS-04 | Listagem em ordem cronológica (mais recente primeiro)            | Integração | datas em ordem decrescente                         | Conforme                            | ✅      |
| TS-05 | Filtro por período (`data_inicio`/`data_fim`)                    | Integração | só itens dentro do intervalo                       | Conforme                            | ✅      |
| TS-06 | Filtro por tipo `receita`                                        | Integração | `200` + só receitas                                | `TypeError` `Decimal - float` (500) | ❌      |
| TS-07 | Filtro por categoria (`Vendas`)                                  | Integração | só itens da categoria                              | Conforme                            | ✅      |
| TS-08 | Filtro por valor mínimo e máximo                                 | Integração | só itens na faixa                                  | Conforme                            | ✅      |
| TS-09 | Resumo de totais sem filtro                                      | Integração | receitas/despesas/saldo corretos                   | Conforme                            | ✅      |
| TS-10 | Totais respeitando filtro que isola um tipo                      | Integração | receitas corretas, despesas `0`                    | `TypeError` `Decimal - float` (500) | ❌      |
| TS-11 | Paginação limita itens (`per_page=2`)                            | Integração | 2 itens, 2 páginas                                 | Conforme                            | ✅      |
| TS-12 | Segunda página continua a ordem                                  | Integração | itens restantes em ordem decrescente               | Conforme                            | ✅      |
| TS-13 | Estado inicial do hook (1ª página, totais de página)             | Unitário   | 12 itens, 5 por página, 3 páginas                  | Conforme                            | ✅      |
| TS-14 | Totais somam receitas, despesas e saldo de tudo                  | Unitário   | 15800 / 10100 / 5700                               | Conforme                            | ✅      |
| TS-15 | Filtro por tipo `receita` (hook)                                 | Unitário   | só receitas, despesas `0`                          | Conforme                            | ✅      |
| TS-16 | Filtro por categoria (hook)                                      | Unitário   | só a categoria escolhida                           | Conforme                            | ✅      |
| TS-17 | Filtro por período (hook)                                        | Unitário   | só itens no intervalo                              | Conforme                            | ✅      |
| TS-18 | Filtro por valor mín/máx (hook)                                  | Unitário   | só itens na faixa                                  | Conforme                            | ✅      |
| TS-19 | Aplicar filtros volta para a 1ª página                           | Unitário   | `paginaAtual = 1`                                  | Conforme                            | ✅      |
| TS-20 | Limpar filtros restaura a listagem completa                      | Unitário   | volta a 12 itens, filtros vazios                   | Conforme                            | ✅      |
| TS-21 | Mudar página avança dentro dos limites                           | Unitário   | `paginaAtual = 2`                                  | Conforme                            | ✅      |
| TS-22 | Mudar página ignora valores fora do intervalo                    | Unitário   | permanece em 1                                     | Conforme                            | ✅      |
| TS-23 | Página exibe os cartões de totais no topo                        | Unitário   | Receitas/Despesas/Saldo na tela                    | Conforme                            | ✅      |
| TS-24 | Página lista a 1ª página (cabeçalho + 5 linhas)                  | Unitário   | "12 transação(ões)" + 6 linhas                     | Conforme                            | ✅      |
| TS-25 | Aplicar filtro de tipo atualiza a listagem                       | Unitário   | "5 transação(ões) encontrada(s)"                   | Conforme                            | ✅      |
| TS-26 | Limpar filtros restaura a listagem na UI                         | Unitário   | volta a "12 transação(ões)"                        | Conforme                            | ✅      |

## 4. Evidências

### Backend — `python -m pytest tests/integration/feature_7 -v`

```
tests/integration/feature_7/test_transaction_history.py::test_historico_sem_company_id PASSED
tests/integration/feature_7/test_transaction_history.py::test_historico_sem_token PASSED
tests/integration/feature_7/test_transaction_history.py::test_historico_lista_da_empresa PASSED
tests/integration/feature_7/test_transaction_history.py::test_historico_ordem_cronologica PASSED
tests/integration/feature_7/test_transaction_history.py::test_historico_filtra_por_periodo PASSED
tests/integration/feature_7/test_transaction_history.py::test_historico_filtra_por_tipo_receita FAILED
tests/integration/feature_7/test_transaction_history.py::test_historico_filtra_por_categoria PASSED
tests/integration/feature_7/test_transaction_history.py::test_historico_filtra_por_valor_minimo_e_maximo PASSED
tests/integration/feature_7/test_transaction_history.py::test_historico_resumo_de_totais PASSED
tests/integration/feature_7/test_transaction_history.py::test_historico_totais_respeitam_filtro FAILED
tests/integration/feature_7/test_transaction_history.py::test_historico_paginacao_limita_itens PASSED
tests/integration/feature_7/test_transaction_history.py::test_historico_segunda_pagina PASSED

E       TypeError: unsupported operand type(s) for -: 'decimal.Decimal' and 'float'
app/services/transaction_service.py:39: TypeError
================== 2 failed, 10 passed, 82 warnings in 6.22s ===================
```

### Frontend — `npx vitest run src/hooks/useTransacoes.test.js src/pages/Transacoes/Transacoes.test.jsx`

```
 ✓ src/hooks/useTransacoes.test.js (10 tests) 28ms
 ✓ src/pages/Transacoes/Transacoes.test.jsx (4 tests) 456ms
 Test Files  2 passed (2)
      Tests  14 passed (14)
```

**Total:** 26 testes — 24 passaram, 2 falharam (documentando **DEF-01**), 0 skip.

## 5. Defeitos encontrados

| ID     | Descrição                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Branch de correção                | Status |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|--------|
| DEF-01 | `get_history_filtered` (`backend/app/services/transaction_service.py:39`) quebra com `TypeError: unsupported operand type(s) for -: 'decimal.Decimal' and 'float'` sempre que o conjunto filtrado tem **só um tipo** de transação. Causa: `sum(<gerador vazio>) or 0.0` devolve `0.0` (float) enquanto o outro total vem como `Decimal` de `func.sum`, e `saldo = receitas - despesas` estoura. Impacto: HTTP **500** ao filtrar por `tipo`, ou quando período/categoria/faixa de valor isolam um único tipo. | `fix/historico-totais-decimal`    | Aberto |
| DEF-02 | `useTransacoes.js` pagina a **5 itens por página** (`POR_PAGINA = 5`), mas o critério de aceitação exige **máximo 20**.                                                                                                                                                                                                                                                                                                                                                                                       | `fix/historico-paginacao-20`      | Aberto |
| DEF-03 | O front opera sobre dados estáticos (`TRANSACOES_MOCK` em `useTransacoes.js`) e **não consome** `GET /api/transactions/` (`transacao.service.js` está vazio). Filtros, totais e paginação não exercitam o backend real; quando integrado, herdará o **DEF-01**.                                                                                                                                                                                                                                               | `fix/historico-integra-front-api` | Aberto |

> Nota (fora do escopo desta feature): a suíte completa do backend tem 3 testes
> vermelhos pré-existentes em `tests/unit/feature_1`
> (`test_register_user_internal_error` e 2× `test_is_valid_password_spaces`).
> São defeitos da **feature 1** — confirmado que falham também sem as mudanças
> desta branch — e devem ser tratados no relatório/issue daquela feature.
>
> Nota (contaminação por outra feature): na suíte de integração completa, os 11
> testes desta feature que passam isolados viram **ERROR** por **contaminação dos
> mappers do SQLAlchemy** — tanto o **DEF-01 da feature 10** (`Simulation` →
> `Company` sem a relação `simulations`) quanto o **DEF-02 da feature 14**
> (`Comparison` → `Company`/`User` sem `comparisons`) quebram a configuração global
> dos mappers ao importar seus models. Devem ser tratados nos relatórios das
> **features 10 e 14**.

## 6. Cobertura

**Backend** — `pytest tests/integration/feature_7 --cov=app.services.transaction_service --cov=app.routes.transaction_routes --cov-report=term-missing`

| Módulo                                | Cobertura | Observação                                                                                                                                                                                         |
|---------------------------------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `app/services/transaction_service.py` | 40%       | a função desta história, `get_history_filtered` (linhas 6-68), é **testada integralmente **; o não-coberto (`71-152`) é `create`/`get_company_transactions`/`update`/`delete`, de outras histórias |
| `app/routes/transaction_routes.py`    | 53%       | o não-coberto é `create`/`update`/`delete` (POST/PUT/DELETE), fora desta história                                                                                                                  |

**Frontend** — `npx vitest run src/hooks/useTransacoes.test.js src/pages/Transacoes/Transacoes.test.jsx --coverage`

| Módulo                                | Cobertura | Linhas não cobertas                                              |
|---------------------------------------|-----------|------------------------------------------------------------------|
| `src/hooks/useTransacoes.js`          | **100%**  | branch da linha 40 (`valorMin`/`valorMax`) parcial               |
| `src/pages/Transacoes/Transacoes.jsx` | 82,6%     | fluxos de modal/edição/exclusão (`246-259`), fora desta história |

Cobertura do núcleo da feature (hook em 100% e `get_history_filtered` totalmente
exercitado) acima da meta de **≥ 60%**.

## 7. Parecer final

**Reprovada.**

A maioria do comportamento está coberta e verde, com o hook de filtros em
100% e a query de histórico totalmente exercitada. Porém **dois critérios de
aceitação centrais falham no backend** por causa do **DEF-01**: filtrar por tipo
e calcular os totais de um período filtrado que isole receitas ou despesas
retornam **HTTP 500** (`Decimal - float`). Como esse é justamente o caso de uso
principal da história ("analisar a situação financeira com filtros"), a feature
não pode ser aprovada como está.

**Próximos passos para reavaliação:**
1. **DEF-01** — corrigir o cálculo dos totais em `get_history_filtered` (normalizar
   tipos antes do `saldo = receitas - despesas`).
2. **DEF-02** — alinhar a paginação do front para 20 itens/página (ou justificar o 5).
3. **DEF-03** — integrar o front ao endpoint real; hoje a tela roda sobre mock.
