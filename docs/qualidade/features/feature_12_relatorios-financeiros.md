# Documentação de Testes - Relatórios Financeiros

---
## 1. Identificação

| Campo                         |  Valor                                                           |
|-------------------------------|------------------------------------------------------------------|
| **Feature**                   | Relatórios Financeiros (US12)                                    |
| **Cenário**                   | CEN-03 - Geração de relatório financeiro                         |
| **Requisito(s)**              | R11                                                              |
| **Branch de desenvolvimento** | `feature/12-relatorios-financeiros`                              |
| **Branch de teste (QA)**      | `test/feature/12-relatorios-financeiros` (a partir da `develop`) |
| **PR / Pipeline**             | GitHub Actions `tests` (run 27774589808) - **success**           |
| **Sprint(s)**                 | 8                                                                |
| **Responsáveis**              | Daniel Filipe / Matheus Moretti                                  |
| **Data**                      | 19/06/2026                                                       |

> A branch de teste foi baseada na `develop` e o código de relatórios (`report_routes/
> schema/service` + página `Relatorios/`) foi trazido da `feature/12` (que estava 49
> commits atrás da `develop`). Para o código subir, foi necessário corrigir o **DEF-01**
> (import quebrado) - ver §5.

---
## 2. Critérios de aceitação testáveis

- [x] **CA-01** Gerar relatório mensal ou anual - `TS-01`, `TS-02`, `TS-14` (back), `TS-18`, `TS-20` (front)
- [~] **CA-02** Exibir total de receitas, despesas e saldo do período - estrutura retornada (`TS-14`), mas os **valores vêm zerados** → **DEF-02** (`TS-16`); front exibe cards estáticos (`TS-17`)
- [ ] **CA-03** Distribuição de gastos por categoria - afetada pelo **DEF-02** (lista vazia); front com gráfico estático
- [~] **CA-04** Evolução do saldo no período - estrutura retornada; valores afetados pelo **DEF-02**
- [x] **CA-05** Filtrar por período personalizado - `TS-03`, `TS-15` (back), `TS-19` (front)
- [x] **CA-06** Considera apenas transações da empresa autenticada - `TS-11` (403 sem acesso) + filtro por `company_id`

---
## 3. Casos executados

| Caso   | Descrição                                             | Nível            | Esperado                                       | Observado                               |     Status     |
|:------:|-------------------------------------------------------|------------------|------------------------------------------------|-----------------------------------------|:--------------:|
| TS-01  | `get_period_dates` período mensal                     | Unitário         | 1º ao último dia do mês                        | Conforme                                |       OK       |
| TS-02  | `get_period_dates` período anual                      | Unitário         | 01/01 a 31/12                                  | Conforme                                |       OK       |
| TS-03  | `get_period_dates` período personalizado              | Unitário         | usa `start`/`end` informados                   | Conforme                                |       OK       |
| TS-04  | `get_period_dates` mensal sem mês/ano                 | Unitário         | `ValueError`                                   | Conforme                                |       OK       |
| TS-05  | `get_period_dates` `start` > `end`                    | Unitário         | `ValueError`                                   | Conforme                                |       OK       |
| TS-06  | `get_period_dates` sem parâmetros                     | Unitário         | `ValueError`                                   | Conforme                                |       OK       |
| TS-07  | `GET /api/reports` sem token                          | Integração       | `401`                                          | Conforme                                |       OK       |
| TS-08  | `GET /api/reports` sem `cnpj`                         | Integração       | `400`                                          | Conforme                                |       OK       |
| TS-09  | `GET /api/reports` com `period` inválido              | Integração       | `400`                                          | Conforme                                |       OK       |
| TS-10  | `GET /api/reports` empresa inexistente                | Integração       | `404`                                          | Conforme                                |       OK       |
| TS-11  | `GET /api/reports` usuário sem acesso à empresa       | Integração       | `403`                                          | Conforme                                |       OK       |
| TS-12  | `GET /api/reports` mensal sem mês/ano                 | Integração       | `400`                                          | Conforme                                |       OK       |
| TS-13  | `GET /api/reports` período invertido (`start`>`end`)  | Integração       | `400`                                          | Conforme                                |       OK       |
| TS-14  | `GET /api/reports` mensal retorna estrutura e período | Integração       | `200` + `periodo/totais/distribuicao/evolucao` | Conforme                                |       OK       |
| TS-15  | `GET /api/reports` período personalizado              | Integração       | `200` + datas corretas                         | Conforme                                |       OK       |
| TS-16  | Totais refletem as transações do período              | Integração       | receitas/despesas/saldo corretos               | Totais zerados (filtro `ENTRADA/SAIDA`) | xfail (DEF-02) |
| TS-17  | Front exibe cards de Receitas, Despesas e Saldo       | Unitário (front) | três cards na tela                             | Conforme                                |       OK       |
| TS-18  | Front (mensal) exibe campo de mês                     | Unitário (front) | `input[type=month]`                            | Conforme                                |       OK       |
| TS-19  | Front (personalizado) exibe dois campos de data       | Unitário (front) | dois `input[type=date]`                        | Conforme                                |       OK       |
| TS-20  | Front (anual) exibe campo de ano                      | Unitário (front) | campo "Ano"                                    | Conforme                                |       OK       |

> **Observação de integração:** a página `Relatorios/` é **estática/mock** (dados
> hardcoded, sem chamadas à API). Os casos de front (`TS-17`…`TS-20`) validam o componente
> isolado; não há cobertura end-to-end (ver **DEF-03**).

---
## 4. Evidências

Execução pela **pipeline** (GitHub Actions, workflow `tests`, run `27774589808`),
artefatos em `testes/relatorio-backend/` e `testes/relatorio-frontend/`.

### Backend - `pytest`

```
tests/unit/feature_12/test_report_period.py ......                  (6 passed)
tests/integration/feature_12/test_report_endpoints.py .........x     (9 passed, 1 xfail)
...
===== 6 failed, 203 passed, 15 xfailed, 1 xpassed, 318 warnings in 48.16s ======
```

- **Os 16 testes da feature passaram** (15 verde + 1 xfail documentando o **DEF-02**).
- As **6 falhas** são **pré-existentes e fora do escopo** - todas em `feature_6`
  (transações). Pertencem ao relatório da feature 6.

### Frontend - `vitest run --coverage`

```
src/pages/Relatorios/Relatorios.test.jsx (4 tests) 334ms
 Test Files  10 passed (10)
      Tests  57 passed | 3 skipped (60)
```

---
## 5. Defeitos encontrados

| Issue   | Descrição                                                                                                                                                                                                                                                                                          | Branch de correção           | Status    |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|-----------|
| DEF-01  | `report_service.py` tinha `from datetime import date, calendar` - `calendar` não existe em `datetime` → **`ImportError`**, impedindo o módulo de carregar (e derrubando o `create_app`). **Corrigido nesta entrega** (`import calendar` / `from datetime import date`) para viabilizar a execução. | (aplicado)                   | Corrigido |
| DEF-02  | `report_service` agrega filtrando `Transaction.type == 'ENTRADA'/'SAIDA'`, mas as transações do sistema usam `'receita'/'despesa'`. Resultado: `totais`, `distribuicao_categorias` e `evolucao` vêm **sempre zerados/vazios**, mesmo com transações no período (CA-02/CA-03/CA-04).                | `fix/report-tipo-transacao`  | Aberto    |
| DEF-03  | A página `Relatorios/` não está integrada à API: usa dados **hardcoded** (sem seletor de período funcional nem chamada a `/api/reports`). Sem consulta real.                                                                                                                                       | `fix/relatorios-integra-api` | Aberto    |

> Fora do escopo entregue: o **export em PDF** (tarefa da issue) não foi implementado.

---
## 6. Cobertura

### Backend - `coverage.xml` (artefato da pipeline)

| Módulo                           | Cobertura (linhas)   |
|----------------------------------|----------------------|
| `app/routes/report_routes.py`    | **100%**             |
| `app/schemas/report_schema.py`   | **100%**             |
| `app/services/report_service.py` | **93,9%**            |

### Frontend - `coverage/` (artefato da pipeline)

| Módulo                                | Cobertura (linhas)   |  Observação                                                     |
|---------------------------------------|----------------------|-----------------------------------------------------------------|
| `src/pages/Relatorios/Relatorios.jsx` | **100%**             | componente estático, totalmente renderizado por `TS-17`…`TS-20` |

Backend bem acima da meta de **≥ 60%**.

---
## 7. Parecer final

> **Status:** Pendente **Aprovada com pendências**
>
> As camadas funcionam individualmente e estão verdes: a casca do endpoint está sólida e
> bem coberta (rotas 100%, schema 100%, service 93,9%) - autenticação (401), validações
> (400), empresa inexistente (404), controle de acesso por empresa (403) e o cálculo de
> datas (mensal/anual/personalizado); no front, o `Relatorios.jsx` renderiza o seletor de
> período e os cards. O **DEF-01** (ImportError) foi corrigido nesta entrega.
>
> As pendências abaixo já estão **encaminhadas nas issues de refatoração em andamento**
> (estabilização/integração) e não bloqueiam a entrega das camadas:
>
> - **DEF-02** - a agregação filtra por `type == 'ENTRADA'/'SAIDA'`, mas as transações
>   usam `'receita'/'despesa'`; com isso `totais`, `distribuicao_categorias` e `evolucao`
>   retornam zero/vazio com dados reais (CA-02/CA-03/CA-04). Correção de baixo esforço.
> - **DEF-03** - a página `Relatorios/` ainda é estática (não integrada à API).
>
> **Pendências para a integração / próxima iteração:**
> 1. **DEF-02** - alinhar o filtro do `report_service` aos valores reais de `Transaction.type`
>    (`'receita'`/`'despesa'`).
> 2. **DEF-03** - integrar a página `Relatorios/` ao endpoint `/api/reports`.
> 3. Implementar o export em PDF (tarefa pendente da issue).
