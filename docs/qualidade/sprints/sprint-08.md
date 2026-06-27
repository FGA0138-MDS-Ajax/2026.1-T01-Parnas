# Consolidado de Testes e GQM - Sprint 8

| Campo | Valor |
|---|---|
| **Sprint** | 8 |
| **Período** | 14-20/jun |
| **Foco** | Centralização documental e relatórios financeiros (CEN-02 e CEN-03, Func. G e F) |

---
## 1. Features testadas

| Feature | Requisito | Status |
| --- | :--: | --- |
| [Centralização documental](../features/feature_9_centralizacao-documental.md) | R10 | Aprovada com pendências |
| [Relatórios financeiros](../features/feature_12_relatorios-financeiros.md) | R11 | Aprovada com pendências |

> A Sprint também concentrou trabalho de **refatoração** transversal (padronização de
> DTOs com Marshmallow e redesign do frontend - [task5](../../issues/task5.md)).

---
## 2. Casos agregados

| Caso | Nível | Status |
| :--: | --- | :--: |
| TS-19 | Integração | OK |
| TS-21 | Integração | Pendente |

## 3. Defeitos

| # | Descrição | Branch | Status |
| :--: | --- | --- | --- |
| 1 | Exportação de relatório em PDF com totais divergentes do dashboard | `fix/relatorio-pdf` | Corrigido |
| 2 | Endpoints sem padronização de schema de saída (dados sensíveis expostos) | `refactor/dtos-redesign` | Em andamento |

## 4. Números gerais

| Indicador | Valor |
| --- | :--: |
| Casos planejados | 2 |
| Casos executados | 2 |
| Casos aprovados | 1 |
| Defeitos encontrados | 2 |

## 5. Cobertura (M3)

```bash
pytest --cov=app tests/
```

| Cobertura | Valor | Mínimo (S6-10) |
| --- | :--: | :--: |
| Back-end | 80% | 75% |
| Front-end | 80% (Vitest) | 75% |
| M3 (média back + front) | 80% | 75% |

## 6. Análise GQM

| Métrica | Valor | Meta |
| :--: | :--: | --- |
| M1 - Throughput | 6 issues | Tendência estável/crescente |
| M2 - Densidade de Defeitos | 0,33 | ≈ 0 |
| M3 - Cobertura | 80% (back 80% / front 80%) | ≥ 75% |
| M4 - Taxa de Aprovação da Pipeline | 83% | ≥ 70% |

## 7. Parecer da dupla

> Documentos e relatórios foram entregues, fechando CEN-02 e CEN-03. A cobertura
> (back e front) chegou a 80% e a pipeline a 83%, ambos acima das metas. A Sprint carregou um esforço
> de refatoração (DTOs e redesign) que segue em andamento e cuja consolidação foi
> planejada para a Sprint de estabilização (S10).
