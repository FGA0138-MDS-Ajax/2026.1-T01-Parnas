# Documentação de Teste - Fix: Integração real da aba Transações (e Contas)

## 1. Identificação

| Campo | Valor |
|---|---|
| **Tarefa** | Integração real das telas de Transações e Contas (remoção dos mocks) |
| **Escopo deste relatório** | Backend (Contas a pagar/receber e rota de transações) e frontend (integração) |
| **Branch de desenvolvimento** | `fix/integracao-transacoes` |
| **Branch base comparada** | `develop` |
| **PR** | #81 (para `develop`) |
| **Sprint** | 10 |
| **Responsáveis (QA)** | Daniel Filipe / Matheus Moretti |
| **Data** | 27/06/2026 |
| **Parecer** | **APROVADA com pendências** (ver §6) |

---
## 2. Escopo

O PR integra de fato as telas de Transações e Contas ao backend, removendo dados
mockados no frontend, e ajusta a camada de Contas a pagar/receber (`BillService`) e a
rota de transações.

---
## 3. Casos executados (backend)

Suíte `tests/integration/feature_11/test_contas_qa.py` (CRUD de contas + quitação + acesso).

| Caso | Descrição | Esperado | Status |
|---|---|---|:--:|
| QA-01 | Criar conta | 201 + `id` | Passou |
| QA-02 | Criar sem token | 401 | Passou |
| QA-03 | Criar faltando campo obrigatório | 400 | Passou |
| QA-04 | Listar contas da empresa | 200 + lista | Passou |
| QA-05 | Listar sem `company_id` | 400 | Passou |
| QA-06 | Quitar conta marca `quitado` (e gera transação) | 200 + status quitado | Passou |
| QA-07 | Não editar conta quitada | 400 | Passou |
| QA-08 | Acesso negado a empresa sem vínculo | 403 | Passou |

**8 testes, 0 falhas.** Além disso, esta branch já corrige (de forma independente) o bug
das rotas de `update`/`delete` de transação (passagem de argumentos na ordem errada para
o service) - convergindo com a correção da task7.

---
## 4. Evidências

```bash
python -m pytest tests/integration/feature_11/test_contas_qa.py -q
# 8 passed

npm run test:run   # frontend
# 28 failed | 65 passed  (ver §5)
```

---
## 5. Defeitos / pendências

| Item | Descrição | Status |
|---|---|---|
| PEND-1 (front) | A reescrita para integração real deixou **28 testes de frontend desatualizados** nos módulos reescritos: `useTransacoes` (10), `Usecontas` (6), `Categorias` (7), `Transacoes` (3), `ContasCaixa` (2). Os testes ainda exercitam as versões antigas (com mocks locais); os hooks/páginas agora dependem de chamadas reais à API e do `EmpresaContext`. São testes desatualizados, não defeitos de funcionalidade. | Aberto |
| PEND-2 (back) | A branch herda da `develop` as falhas pré-existentes de feature_4/6/8 (escopo da task7). | Aberto |

**Como ajeitar rápido (frontend):** nos testes dos módulos reescritos, mockar os
`services` novos (`categoria.service`, `conta.service`, etc.) e prover o `EmpresaContext`
com uma empresa ativa, em vez de passar listas mockadas diretas. Ex.: o
`useTransacoes.test.js` precisa de empresa ativa para `listarCategorias` não lançar
"Selecione uma empresa para carregar as categorias.".

---
## 6. Parecer final

> **Status:** Aprovada com pendências
>
> A integração funciona: o backend de Contas (CRUD + quitação + controle de acesso) passa
> em todos os casos de QA (8/8) e a branch ainda corrige o bug das rotas de transação. A
> pendência é a atualização dos 28 testes de frontend dos módulos reescritos (test-lag da
> remoção de mocks) e as falhas de backend herdadas da `develop` (task7). Recomenda-se
> reconciliar os testes antes/junto do merge.
