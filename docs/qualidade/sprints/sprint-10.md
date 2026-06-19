# Consolidado de Testes e GQM - Sprint 10

| Campo | Valor |
|---|---|
| **Sprint** | 10 |
| **Período** | 28/jun-04/jul |
| **Foco** | Estabilização, refatoração e entrega final - testes E2E (Playwright) e carga (Locust) |

> **Sprint de estabilização, ainda não iniciada.** Concentra a consolidação dos
> defeitos mapeados nas Sprints anteriores, a refatoração das integrações e os testes
> E2E e de carga. Os valores de GQM serão *projetados/consolidados* no fechamento.

---
## 1. Features testadas

| Feature | Requisito | Status |
| --- | :--: | --- |
| *Reexecução do roteiro completo (regressão)* | R01-R15 | *a preencher* |

---
## 2. Casos agregados

| Caso | Nível | Status |
| :--: | --- | :--: |
| TS-24 | Sistema | *a preencher* |
| TS-25 | Sistema | *a preencher* |
| TS-26 | Sistema | *a preencher* |
| TS-27 | Carga | *a preencher* |

## 3. Defeitos (consolidação)

| # | Descrição | Branch | Status |
| :--: | --- | --- | --- |
| 1 | Integração da aba de Transações com a API | `fix/integracao-transacoes` | *a preencher* |
| 2 | Exclusão de conta não invalida a sessão | `fix/exclusao-conta-sessao` | *a preencher* |
| 3 | Diferenciação entre Contas e Transações | `fix/diferenciacao-contas-transacoes` | *a preencher* |
| 4 | Consolidação das integrações entre classes | `refactor/integracao-classes` | *a preencher* |

## 4. Números gerais

| Indicador | Valor |
| --- | :--: |
| Casos planejados | *a preencher* |
| Casos executados | *a preencher* |
| Casos aprovados | *a preencher* |
| Defeitos encontrados | *a preencher* |

## 5. Cobertura (M3)

```bash
pytest --cov=app tests/
```

| Cobertura | Valor | Mínimo (S6-10) |
| --- | :--: | :--: |
| Back-end | *-%* | 75% |
| Front-end | n/d (Vitest a configurar) | 75% |

## 6. Análise GQM

| Métrica | Valor | Meta |
| :--: | :--: | --- |
| M1 - Throughput | *a preencher* | Tendência estável/crescente |
| M2 - Densidade de Defeitos | *a preencher* | ≈ 0 |
| M3 - Cobertura | *a preencher* | ≥ 75% |
| M4 - Taxa de Aprovação da Pipeline | *a preencher* | ≥ 70% |

## 7. Parecer da dupla

> *a preencher ao final da Sprint.*
