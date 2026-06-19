# Consolidado de Testes e GQM - Sprint 9

| Campo | Valor |
|---|---|
| **Sprint** | 9 |
| **Período** | 21-27/jun |
| **Foco** | Diagnóstico e simulação de crédito (CEN-04, Func. H e I) |

---
## 1. Features testadas

| Feature | Requisito | Status |
| --- | :--: | --- |
| [Simulação de crédito (front + back)](../features/feature_10_e_13_simulacao-credito.md) | R12 | Aprovada com pendências |
| [Comparação de modalidades de crédito](../features/feature_14_modalidades-credito.md) | R13 | Aprovada com pendências |

---
## 2. Casos agregados

| Caso | Nível | Status |
| :--: | --- | :--: |
| TS-06 | Unitário | OK |
| TS-07 | Unitário | OK |
| TS-08 | Unitário | OK |
| TS-09 | Unitário | OK |
| TS-10 | Unitário | OK |
| TS-22 | Integração | OK |
| TS-23 | Integração | OK |
| TS-26 | Sistema | Pendente |

## 3. Defeitos

| # | Descrição | Branch | Status |
| :--: | --- | --- | --- |
| 1 | Divergência de contrato entre front e back na simulação/comparação (campos e nomes de payload) | `fix/contrato-credito` | Em aberto (S10) |

## 4. Números gerais

| Indicador | Valor |
| --- | :--: |
| Casos planejados | 8 |
| Casos executados | 7 |
| Casos aprovados | 7 |
| Defeitos encontrados | 1 |

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
| M2 - Densidade de Defeitos | 0,17 | aprox. 0 |
| M3 - Cobertura | 80% (back 80% / front 80%) | maior ou igual a 75% |
| M4 - Taxa de Aprovação da Pipeline | 85% | maior ou igual a 70% |

## 7. Parecer da dupla

> A simulação (Price/SAC e projeção de fluxo) e a comparação de modalidades foram
> aprovadas com pendências: a lógica de cálculo passou em unidade e os endpoints em
> integração, mas há divergência de contrato entre front e back, registrada como
> `fix/contrato-credito` para a estabilização. A densidade de defeitos caiu para 0,17
> e o M3 médio (back 80% / front 80%) ficou em 80%, acima do mínimo de 75%. O E2E de
> crédito (TS-26) ficou planejado para a Sprint 10.
