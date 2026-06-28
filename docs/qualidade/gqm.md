# Modelo GQM

O grupo usa o método **GQM (Goal-Question-Metric)** para medir a qualidade do
processo e do produto. A cada Sprint as métricas são coletadas e analisadas no
[consolidado da Sprint](sprints/index.md).

---
## Estrutura GQM

```
Goal (Meta)
  └─ Question (Pergunta)
        └─ Metric (Métrica)
```

**Meta geral:** garantir a entrega contínua de incrementos do CrediFab com
qualidade controlada, defeitos sob controle e cobertura de testes crescente.

| Pergunta                                         | Métrica                                |
|--------------------------------------------------|----------------------------------------|
| O time está entregando trabalho a cada Sprint?   | **M1 - Throughput**                    |
| A qualidade do que é entregue está sob controle? | **M2 - Densidade de Defeitos**         |
| O código está coberto por testes?                | **M3 - Cobertura**                     |
| O processo de integração está saudável?          | **M4 - Taxa de Aprovação da Pipeline** |

---
## Métricas

### M1 - Throughput

Número de **issues movidas para *Done*** por Sprint.

```
M1 = nº de issues concluídas na Sprint
```

Indica a vazão do time. Acompanhado ao longo das Sprints para identificar
tendência (estável, crescente, queda).

### M2 - Densidade de Defeitos

```
M2 = nº de bugs (label `bug`) / nº de issues concluídas
```

- **Ideal:** ≈ 0.
- Mede a proporção de retrabalho/defeitos em relação ao entregue.

### M3 - Cobertura de testes

Média entre a cobertura de back-end (`pytest-cov`) e de front-end
(`vitest --coverage`).

```
M3 = média( cobertura_backend , cobertura_frontend )
```

| Período      | Mínimo exigido |
|--------------|:--------------:|
| Sprints 1-5  |    **60%**     |
| Sprints 6-10 |    **75%**     |

> O Vitest gera cobertura de front-end desde o início, então M3 é a média entre
> back-end (pytest-cov) e front-end (Vitest) em todas as Sprints.

### M4 - Taxa de Aprovação da Pipeline

```
M4 = PRs aprovados no 1º run / total de PRs
```

- **Meta:** ≥ **70%** a partir da Sprint 5.
- Depende da existência da pipeline de CI de testes (pendência atual).

## Tabela-resumo

| Métrica   | Definição                      | Meta                        |
|:---------:|--------------------------------|-----------------------------|
|    M1     | Issues concluídas por Sprint   | Tendência estável/crescente |
|    M2     | Bugs / issues concluídas       | ≈ 0                         |
|    M3     | Cobertura média (back + front) | ≥ 60% (S1-5), ≥ 75% (S6-10) |
|    M4     | PRs aprovados no 1º run        | ≥ 70% (a partir da S5)      |

---
## Evolução por Sprint

Valores coletados em cada [consolidado de Sprint](sprints/index.md). M3 é a média
entre a cobertura de back-end (pytest-cov) e a de front-end (Vitest).

| Sprint   | M1 (issues) |  M2 (defeitos/issue) | Cob. back  | Cob. front |  M3 (média) |      M4 (pipeline)      |
|:--------:|:-----------:|:--------------------:|:----------:|:----------:|:-----------:|:-----------------------:|
|    4     |      5      |         0,40         |    63%     |    62%     |     63%     | n/d (CI em implantação) |
|    5     |      6      |         0,33         |    69%     |    67%     |     68%     |           67%           |
|    6     |      6      |         0,33         |    73%     |    78%     |     76%     |           72%           |
|    7     |      7      |         0,29         |    77%     |    79%     |     78%     |           79%           |
|    8     |      6      |         0,33         |    80%     |    80%     |     80%     |           83%           |
|    9     |      6      |         0,17         |    80%     |    80%     |     80%     |           85%           |
|    10    |  projetada  |      projetada       | 82% (proj) | 82% (proj) | 82% (proj)  |        projetada        |

Leitura geral: throughput (M1) estável entre 5 e 7 issues por Sprint; densidade de
defeitos (M2) em queda (0,40 -> 0,17); pipeline (M4) acima de 70% a partir da Sprint 6.
O M3 médio (back + front) cresceu de 63% para 80% e ficou **acima do mínimo em todas as
Sprints** (60% nas S1-5, 75% nas S6-10), com a cobertura de front-end acompanhando a de
back-end. A Sprint 10
(estabilização) consolida os fixes em aberto e os testes E2E e de carga.

A coleta e o parecer de cada Sprint ficam em
[Consolidados por Sprint](sprints/index.md).

---