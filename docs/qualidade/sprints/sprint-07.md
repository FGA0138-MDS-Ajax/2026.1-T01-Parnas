# Consolidado de Testes e GQM - Sprint 7

| Campo       |  Valor                                                                             |
|-------------|------------------------------------------------------------------------------------|
| **Sprint**  | 7                                                                                  |
| **Período** | 07-13/jun                                                                          |
| **Foco**    | Dashboard, contas a pagar/receber e seleção de empresa ativa (CEN-01, Func. E e J) |

---
## 1. Features testadas

| Feature                                                                     | Requisito   |  Status                 |
|-----------------------------------------------------------------------------|:-----------:|-------------------------|
| [Dashboard financeiro](../features/feature_16_dashboard-financeiro.md)      |     R09     | Aprovada                |
| [Cadastro de contas](../features/feature_11_cadastro-contas.md)             |     R15     | Aprovada com pendências |
| [Seleção de empresa ativa](../features/feature_15_selecao-empresa-ativa.md) |     R04     | Aprovada                |

---
## 2. Casos agregados

|  Caso   | Nível      | Status   |
|:-------:|------------|:--------:|
| TS-20   | Integração |    OK    |
|  TS-18  | Integração |    OK    |
|  TS-17  | Integração |    OK    |

## 3. Defeitos

| #   | Descrição                                                         | Branch                                |  Status         |
|:---:|-------------------------------------------------------------------|---------------------------------------|-----------------|
|  1  | Ambiguidade entre as telas de Contas e Transações                 | `fix/diferenciacao-contas-transacoes` | Corrigido (S10) |
|  2  | Conta quitada não gerava a transação vinculada em todos os fluxos | `fix/quitar-conta`                    | Corrigido       |

## 4. Números gerais

| Indicador            |  Valor |
|----------------------|:------:|
| Casos planejados     |   3    |
| Casos executados     |   3    |
| Casos aprovados      |   3    |
| Defeitos encontrados |   2    |

## 5. Cobertura (M3)

```bash
pytest --cov=app tests/
```

| Cobertura               |   Valor      | Mínimo (S6-10) |
|-------------------------|:------------:|:--------------:|
| Back-end                |     77%      |      75%       |
| Front-end               | 79% (Vitest) |      75%       |
| M3 (média back + front) |     78%      |      75%       |

## 6. Análise GQM

|              Métrica               |          Valor             | Meta                        |
|:----------------------------------:|:--------------------------:|-----------------------------|
|          M1 - Throughput           |          7 issues          | Tendência estável/crescente |
|     M2 - Densidade de Defeitos     |            0,29            | ≈ 0                         |
|           M3 - Cobertura           | 78% (back 77% / front 79%) | ≥ 75%                       |
| M4 - Taxa de Aprovação da Pipeline |            79%             | ≥ 70%                       |

## 7. Parecer da dupla

> Sprint de maior throughput (7 issues) e menor densidade de defeitos até aqui (0,29),
> indicando amadurecimento do pareamento e dos testes. O M3 médio (78%, back 77% /
> front 79%) superou o mínimo de 75% e a pipeline atingiu 79%. A pendência principal é a ambiguidade entre
> Contas e Transações, encaminhada como `fix/` para a estabilização.
