# Resumo de Métricas

Esta página reúne, em um só lugar, **todas as métricas de qualidade** coletadas pela
dupla ao longo do projeto CrediFab. É a visão executiva: para o detalhamento por
Sprint, ver os [Consolidados por Sprint](sprints/index.md); para as definições, o
[Modelo GQM](gqm.md).

> Todas as metas foram atingidas no fechamento (Sprint 10). O projeto foi entregue com
> a suíte de testes verde e as métricas GQM dentro dos limites definidos.

---
## Panorama final (Sprint 10)

| Métrica                          |  Resultado final  |         Meta         | Situação   |
|----------------------------------|:-----------------:|:--------------------:|------------|
| M1 - Throughput                  | 6 issues/Sprint   | Estável/crescente    | Atingida   |
| M2 - Densidade de defeitos       | 0,00              | ≈ 0                  | Atingida   |
| M3 - Cobertura (back + front)    | 82%               | ≥ 75% (S6-10)        | Atingida   |
| M4 - Aprovação da pipeline       | 88%               | ≥ 70%                | Atingida   |

---
## Evolução das métricas (M1-M4)

| Sprint | M1 (issues) | M2 (def/issue) | Cob. back | Cob. front | M3 (média) | M4 (pipeline) |
|:------:|:-----------:|:--------------:|:---------:|:----------:|:----------:|:-------------:|
|   4    |      5      |      0,40      |    63%    |    62%     |    63%     |     n/d       |
|   5    |      6      |      0,33      |    69%    |    67%     |    68%     |     67%       |
|   6    |      6      |      0,33      |    73%    |    78%     |    76%     |     72%       |
|   7    |      7      |      0,29      |    77%    |    79%     |    78%     |     79%       |
|   8    |      6      |      0,33      |    80%    |    80%     |    80%     |     83%       |
|   9    |      6      |      0,17      |    80%    |    80%     |    80%     |     85%       |
|   10   |      6      |      0,00      |    82%    |    82%     |    82%     |     88%       |

Leitura: throughput estável (5-7 issues por Sprint), densidade de defeitos em queda
contínua até zerar, cobertura média subindo de 63% para 82% (sempre acima do mínimo) e
pipeline consistentemente acima de 70% a partir da Sprint 6.

---
## Cobertura de testes por nível

A suíte segue a **pirâmide de testes**: base larga de unitários, camada intermediária
de integração e um topo enxuto de E2E de sistema, com carga sob o topo.

| Nível              | Casos (roteiro) | Ferramenta                     |
|--------------------|:---------------:|--------------------------------|
| Unitário           |       11        | Pytest + pytest-mock / Vitest  |
| Integração         |       12        | Pytest + client Flask          |
| Sistema (E2E)      |        3        | Pytest + client Flask          |
| Carga              |        1        | Locust                         |
| **Total planejado**|     **27**      | -                              |

---
## Números consolidados de execução

| Indicador                         | Valor |
|-----------------------------------|:-----:|
| Casos de teste planejados (TS)    |  27   |
| Casos executados                  |  27   |
| Casos aprovados                   |  27   |
| Defeitos abertos ao final         |   0   |
| Defeitos corrigidos no projeto    |   4   |
| Sprints com M3 acima do mínimo    | 7 / 7 |

---
## Como as métricas são coletadas

| Métrica | Fonte                                                        |
|:-------:|--------------------------------------------------------------|
|   M1    | Issues movidas para *Done* no board por Sprint               |
|   M2    | Issues com label `bug` sobre o total de issues concluídas    |
|   M3    | `pytest --cov` (back) e `vitest --coverage` (front), média   |
|   M4    | PRs aprovados no 1º run da pipeline sobre o total de PRs      |

O detalhamento e o parecer de cada Sprint ficam nos
[Consolidados por Sprint](sprints/index.md).
