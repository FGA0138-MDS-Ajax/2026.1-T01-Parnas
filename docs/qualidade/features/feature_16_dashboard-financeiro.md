# Documentação de Testes - Dashboard Financeiro

---
## 1. Identificação

| Campo | Valor |
|---|---|
| **Feature** | Dashboard Financeiro |
| **Cenário** | CEN-01 |
| **Requisito(s)** | R09 |
| **Branch de desenvolvimento** | `feature/16-dashboard-financeiro` |
| **Branch de teste** | `feature/16-dashboard-financeiro` (testes de QA commitados na própria branch) |
| **PR** | #80 (para `develop`) |
| **Sprint(s)** | 7 |
| **Responsáveis** | Daniel Filipe / Matheus Moretti |
| **Data** | 27/06/2026 |

---
## 2. Critérios de aceitação testáveis

> Acordados com a dupla de desenvolvimento no início da feature.

- [x] `GET /api/dashboard` é protegido por JWT (401 sem token)
- [x] `company_id` é obrigatório na query (400 quando ausente)
- [ ] A resposta traz `saldo_consolidado_atual`, `mes_referencia`, `totais_mes_atual`, `grafico_categorias_mes` e `contas_proximas_vencimento`
- [ ] O saldo consolidado soma as entradas e subtrai as saídas das transações da empresa

---
## 3. Casos executados

Suíte `tests/integration/feature_16/test_dashboard.py` (rota + service + BD em memória).

| Caso | Descrição | Nível | Esperado | Observado | Status |
| :--: | --- | --- | --- | --- | :--: |
| QA-01 | Acesso sem token | Integração | 401 | 401 | Passou |
| QA-02 | `company_id` ausente | Integração | 400 + `erros_de_validacao` | 400 | Passou |
| QA-03 | Estrutura da resposta | Integração | 200 + 5 campos | 500 (KeyError) | Falhou |
| QA-04 | Saldo consolidado (receita 300 - despesa 100 = 200) | Integração | 200 + saldo 200.0 | 500 (KeyError) | Falhou |

---
## 4. Evidências

```bash
python -m pytest tests/integration/feature_16 -q
# 2 failed, 2 passed
```

Erro observado em QA-03/QA-04 (a chamada estoura antes de montar a resposta):

```
incomes = float(summary.total_receitas or 0)
KeyError: 'total_receitas'
```

---
## 5. Defeitos encontrados

| Issue | Descrição | Status |
|---|---|---|
| DEF-D1 | `dashboard_service.get_consolidated_balance`: a query rotula as colunas como `total_incomes`/`total_expenses`, mas o código lê `summary.total_receitas`/`total_despesas` -> `KeyError`, derrubando o endpoint com 500. | Aberto |
| DEF-D2 | Inconsistência de tipos: `dashboard_service` e `report_service` somam transações com `type` `'ENTRADA'/'SAIDA'`, mas o `transaction_service` grava `'receita'/'despesa'`. Mesmo após corrigir DEF-D1, o saldo viria 0 para dados reais. (Inconsistência mais ampla, também presente na `develop`.) | Aberto |

**Como corrigir (rápido) - `backend/app/services/dashboard_service.py`:**

```python
# usar os nomes dos labels da query (total_incomes/total_expenses)
incomes = float(summary.total_incomes or 0)
expenses = float(summary.total_expenses or 0)
# e alinhar os tipos com o que o TransactionService grava:
case((Transaction.type == 'receita', Transaction.amount), else_=0)  # entradas
case((Transaction.type == 'despesa', Transaction.amount), else_=0)  # saidas
```

---
## 6. Cobertura

| Métrica | Valor |
|---|---|
| Cobertura da feature | Contrato (auth/validação) coberto; cálculo do saldo bloqueado pelo DEF-D1 |

---
## 7. Parecer final

> **Status:** Reprovada
>
> O contrato de autenticação e validação do endpoint funciona, mas o cálculo do saldo
> consolidado quebra com `KeyError` (DEF-D1), retornando 500 - o coração do dashboard não
> responde. Há ainda a inconsistência de tipos (DEF-D2). Os testes de QA já estão
> commitados na branch e passarão assim que DEF-D1 e DEF-D2 forem corrigidos. Não mesclar
> até a correção.
