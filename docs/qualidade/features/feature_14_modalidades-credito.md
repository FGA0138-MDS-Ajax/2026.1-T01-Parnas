# Relatório de QA — Feature 14: Comparação de Modalidades de Crédito

## 1. Identificação

| Campo | Valor |
|---|---|
| **Feature** | US14 — Comparação de modalidades de crédito |
| **Cenário** | CEN-04 — Diagnóstico e simulação de crédito |
| **Requisito** | R13 |
| **Sprint** | 9 |
| **Branch de desenvolvimento** | `feature/14-modalidades-credito` |
| **Branch de teste (QA)** | `test/feature/14-modalidades-credito` (a partir da `develop`) |
| **PR / Pipeline** | GitHub Actions `tests` (run 27777463269) — **success** |
| **Responsáveis (QA)** | Daniel Filipe / Matheus Moretti |
| **Data** | 18/06/2026 |

> **Reavaliação.** Esta feature havia sido **reprovada** por 3 defeitos (DEF-01 blueprint
> não registrado, DEF-02 mappers, DEF-03 `reportlab` não declarado). Todos foram
> **corrigidos** (DEF-02/DEF-03 pelo time de desenvolvimento — `backref` e dependência no
> `requirements`; DEF-01 no registro do blueprint durante a integração na `develop`).
> O front passou a consumir a API real (`/api/comparacoes/*`).

## 2. Critérios de aceitação testáveis

- [x] **CA-01** Adicionar até 4 modalidades para comparar — `TS-07`, `TS-09` (limite), `TS-17` (front)
- [x] **CA-02** Cada modalidade tem nome, taxa de juros, prazo e tipo (PF/PJ) — `TS-08`
- [x] **CA-03** Calcula parcela, total pago e total de juros para cada — `TS-01`, `TS-02`, `TS-08`
- [x] **CA-04** Destaca visualmente a modalidade mais vantajosa (menor custo) — `TS-03`, `TS-08`
- [x] **CA-05** Alerta quando a modalidade é de pessoa física — `TS-04`, `TS-05`, `TS-08`
- [x] **CA-06** Exporta a comparação como PDF — `TS-15`, `TS-16`
- [x] **(Persistência)** Salvar, listar e excluir comparações da empresa — `TS-11`…`TS-14`

## 3. Casos executados

| Caso | Descrição | Nível | Esperado | Observado | Status |
| :--: | --- | --- | --- | --- | :--: |
| TS-01 | `_calculate_price_table` com taxa 0 | Unitário | parcela = valor/prazo, juros 0 | Conforme | ✅ |
| TS-02 | `_calculate_price_table` com juros | Unitário | juros > 0 e total > valor | Conforme | ✅ |
| TS-03 | `calculate_simulation` marca a de menor custo como melhor | Unitário | uma `is_best_option=True` (a mais barata) | Conforme | ✅ |
| TS-04 | `calculate_simulation` sinaliza modalidade PF | Unitário | `warning_pf=True`, `type='PF'` | Conforme | ✅ |
| TS-05 | `calculate_simulation` PJ não dispara alerta | Unitário | `warning_pf=False` | Conforme | ✅ |
| TS-06 | `calculate_simulation` sem modalidades | Unitário | `400` | Conforme | ✅ |
| TS-07 | `calculate_simulation` com 5 modalidades | Unitário | `400` (limite de 4) | Conforme | ✅ |
| TS-08 | `POST /api/comparacoes/calcular` retorna comparação, melhor opção e alerta PF | Integração | `200` + métricas por modalidade | Conforme | ✅ |
| TS-09 | `POST /calcular` com mais de 4 modalidades | Integração | `400` | Conforme | ✅ |
| TS-10 | `POST /calcular` sem token | Integração | `401` | Conforme | ✅ |
| TS-11 | `POST /api/comparacoes` salva a comparação | Integração | `201` + `id` | Conforme | ✅ |
| TS-12 | `GET /api/comparacoes` lista as da empresa | Integração | `200` + comparação salva | Conforme | ✅ |
| TS-13 | `DELETE /api/comparacoes/<id>` existente | Integração | `200`, some da lista | Conforme | ✅ |
| TS-14 | `DELETE /api/comparacoes/<id>` inexistente | Integração | `404` | Conforme | ✅ |
| TS-15 | `GET /api/comparacoes/<id>/exportar` existente | Integração | `200` + `application/pdf` | Conforme | ✅ |
| TS-16 | `GET /api/comparacoes/<id>/exportar` inexistente | Integração | `404` | Conforme | ✅ |
| TS-17 | Front começa com 1 modalidade e adiciona outra | Unitário (front) | "Modalidade 2" aparece | Conforme | ✅ |
| TS-18 | Front: calcular sem valor não chama o serviço | Unitário (front) | serviço não chamado (feedback de erro) | Conforme | ✅ |
| TS-19 | Front: calcular com dados válidos chama o serviço | Unitário (front) | `calcularComparacao` chamado | Conforme | ✅ |

## 4. Evidências

Execução pela **pipeline** (GitHub Actions, workflow `tests`, run `27777463269`),
artefatos em `testes/relatorio-backend/` e `testes/relatorio-frontend/`.

### Backend — `pytest`

```
tests/unit/feature_14/test_comparison_service.py .......            (7 passed)
tests/integration/feature_14/test_comparison_endpoints.py .........  (9 passed)
...
===== 6 failed, 219 passed, 15 xfailed, 1 xpassed, 344 warnings in 51.68s ======
```

- **Os 16 testes da feature passaram** (sem xfail, sem defeito).
- As **6 falhas** são **pré-existentes e fora do escopo** — todas em `feature_6` (transações).
- Não há mais contaminação de outras features (o DEF-02, que derrubava a `feature_7`, foi resolvido).

### Frontend — `vitest run --coverage`

```
✓ src/pages/Comparacoes/Comparacoes.test.jsx (3 tests) 587ms
 Test Files  11 passed (11)
      Tests  60 passed | 3 skipped (63)
```

## 5. Defeitos encontrados

Nenhum defeito **novo**. Os três defeitos que reprovaram a feature na avaliação anterior
foram corrigidos e **reverificados**:

| ID | Descrição (anterior) | Status |
|---|---|---|
| DEF-01 | `comparison_bp` não registrado → API toda 404 | ✅ Resolvido (blueprint registrado em `/api/comparacoes`) |
| DEF-02 | `back_populates='comparisons'` sem Company/User declararem → quebra de mappers e contaminação da `feature_7` | ✅ Resolvido (`backref='credit_comparisons'`) |
| DEF-03 | `reportlab` importado mas não declarado | ✅ Resolvido (`reportlab==4.5.1` no `requirements.txt`) |

## 6. Cobertura

### Backend — `coverage.xml` (artefato da pipeline)

| Módulo | Cobertura (linhas) |
|---|---|
| `app/models/comparison.py` | **100%** |
| `app/routes/comparison_routes.py` | **100%** |
| `app/services/comparison_service.py` | **99%** |
| `app/repositories/comparison_repository.py` | **0%** (não utilizado pelo service — ver pendências) |

### Frontend — `coverage/` (artefato da pipeline)

| Módulo | Cobertura (linhas) | Observação |
|---|---|---|
| `src/pages/Comparacoes/Comparacoes.jsx` | **86,0%** | não cobertos: ramos de salvar/exportar e renderização do gráfico |

Núcleo da feature (service 99%, página 86%) bem acima da meta de **≥ 60%**.

## 7. Parecer final

> **Status:** 🚧 **Aprovada com pendências**
>
> A feature está **funcional ponta a ponta**: cálculo pela Tabela Price (com e sem juros),
> identificação da modalidade mais vantajosa, alerta de pessoa física, limite de 4
> modalidades, persistência (salvar/listar/excluir) e exportação em PDF — 16 testes de
> backend verdes (cobertura 99–100% nos módulos relevantes). O front consome a API real
> (`/api/comparacoes/*`) e tem 3 testes de componente verdes (86%). Os **três defeitos** da
> avaliação anterior foram corrigidos e reverificados, e a contaminação da suíte (feature 7)
> deixou de ocorrer.
>
> **Pendências (menores, não bloqueiam):**
> 1. `comparison_repository.py` está sem uso (0% de cobertura) — o service acessa o ORM
>    diretamente; recomenda-se remover o repositório ou passar a usá-lo.
> 2. Sem teste E2E (Playwright) — aceitável por não ser fluxo crítico.
