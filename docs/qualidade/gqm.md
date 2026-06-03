# Modelo GQM

O grupo usa o método **GQM (Goal–Question–Metric)** para medir a qualidade do
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

| Pergunta | Métrica |
| --- | --- |
| O time está entregando trabalho a cada Sprint? | **M1 — Throughput** |
| A qualidade do que é entregue está sob controle? | **M2 — Densidade de Defeitos** |
| O código está coberto por testes? | **M3 — Cobertura** |
| O processo de integração está saudável? | **M4 — Taxa de Aprovação da Pipeline** |

---
## Métricas

### M1 — Throughput

Número de **issues movidas para *Done*** por Sprint.

```
M1 = nº de issues concluídas na Sprint
```

Indica a vazão do time. Acompanhado ao longo das Sprints para identificar
tendência (estável, crescente, queda).

### M2 — Densidade de Defeitos

```
M2 = nº de bugs (label `bug`) / nº de issues concluídas
```

- **Ideal:** ≈ 0.
- Mede a proporção de retrabalho/defeitos em relação ao entregue.

### M3 — Cobertura de testes

Média entre a cobertura de back-end (`pytest-cov`) e de front-end
(`vitest --coverage`).

```
M3 = média( cobertura_backend , cobertura_frontend )
```

| Período | Mínimo exigido |
| --- | :--: |
| Sprints 1–5 | **60%** |
| Sprints 6–10 | **75%** |

> Enquanto o front-end não tiver Vitest configurado, M3 considera apenas a
> cobertura de back-end, registrando explicitamente essa limitação.

### M4 — Taxa de Aprovação da Pipeline

```
M4 = PRs aprovados no 1º run / total de PRs
```

- **Meta:** ≥ **70%** a partir da Sprint 5.
- Depende da existência da pipeline de CI de testes (pendência atual).

## Tabela-resumo

| Métrica | Definição | Meta |
| :--: | --- | --- |
| M1 | Issues concluídas por Sprint | Tendência estável/crescente |
| M2 | Bugs / issues concluídas | ≈ 0 |
| M3 | Cobertura média (back + front) | ≥ 60% (S1–5), ≥ 75% (S6–10) |
| M4 | PRs aprovados no 1º run | ≥ 70% (a partir da S5) |

A coleta e o parecer de cada Sprint ficam em
[Consolidados por Sprint](sprints/index.md).

---