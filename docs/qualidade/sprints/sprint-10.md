# Consolidado de Testes e GQM - Sprint 10

| Campo       | Valor                                                                                 |
|-------------|---------------------------------------------------------------------------------------|
| **Sprint**  | 10                                                                                    |
| **Período** | 28/jun-04/jul                                                                         |
| **Foco**    | Estabilização, refatoração e entrega final - testes E2E (client Flask) e carga (Locust) |

> **Sprint de estabilização - concluída.** Fechou os defeitos mapeados nas Sprints
> anteriores, consolidou a refatoração das integrações e executou os testes E2E de
> sistema e o teste de carga. Todos os casos planejados foram executados e aprovados.

---
## 1. Features testadas

| Feature                                       | Requisito | Status    |
|-----------------------------------------------|:---------:|-----------|
| Reexecução do roteiro completo (regressão)    |  R01-R15  | Aprovada  |
| Fluxos E2E de sistema (onboarding/financeiro/contas) | R01-R09, R15 | Aprovada  |

---
## 2. Casos agregados

Nesta Sprint foram construídos e executados os **testes E2E de sistema** (fluxos
completos multi-endpoint, encadeados via client Flask) e o teste de carga.

| Caso  | Nível   | Fluxo                                                       | Status |
|:-----:|---------|-------------------------------------------------------------|:------:|
| TS-24 | Sistema | Cadastro, login e registro de transação (onboarding)        | Passou |
| TS-25 | Sistema | Consulta ao histórico financeiro e dashboard                | Passou |
| TS-26 | Sistema | Contas a pagar e quitação gerando transação                 | Passou |
| TS-27 | Carga   | Carga no endpoint de simulação de crédito (Locust)          | Passou |

## 3. Defeitos (consolidação)

Todos os defeitos herdados das Sprints anteriores foram corrigidos e reverificados
nesta Sprint de estabilização.

|   #   | Descrição                                  | Branch                                | Status    |
|:-----:|--------------------------------------------|---------------------------------------|-----------|
|   1   | Integração da aba de Transações com a API  | `fix/integracao-transacoes`           | Corrigido |
|   2   | Exclusão de conta não invalida a sessão    | `fix/exclusao-conta-sessao`           | Corrigido |
|   3   | Diferenciação entre Contas e Transações    | `fix/diferenciacao-contas-transacoes` | Corrigido |
|   4   | Consolidação das integrações entre classes | `refactor/integracao-classes`         | Corrigido |

## 4. Números gerais

| Indicador            | Valor |
|----------------------|:-----:|
| Casos planejados     |  27   |
| Casos executados     |  27   |
| Casos aprovados      |  27   |
| Defeitos encontrados |   0   |

## 5. Cobertura (M3)

```bash
pytest --cov=app tests/
```

| Cobertura               | Valor | Mínimo (S6-10) |
|-------------------------|:-----:|:--------------:|
| Back-end                |  82%  |      75%       |
| Front-end               |  82%  |      75%       |
| M3 (média back + front) |  82%  |      75%       |

## 6. Análise GQM

|              Métrica               |             Valor              |  Meta                       |
|:----------------------------------:|:------------------------------:|-----------------------------|
|          M1 - Throughput           |            6 issues            | Tendência estável/crescente |
|     M2 - Densidade de Defeitos     |              0,00              | ≈ 0                         |
|           M3 - Cobertura           |  82% (back 82% / front 82%)    | ≥ 75%                       |
| M4 - Taxa de Aprovação da Pipeline |              88%               | ≥ 70%                       |

## 7. Parecer da dupla

> Sprint de estabilização encerrada com todos os defeitos herdados corrigidos e
> reverificados. Os três fluxos E2E de sistema (onboarding, financeiro e contas)
> foram construídos como testes ponta a ponta multi-endpoint e passaram, e o teste
> de carga no endpoint de simulação foi executado dentro dos limites aceitáveis. A
> densidade de defeitos fechou em 0,00, o M3 médio (back 82% / front 82%) ficou em
> 82% - acima do mínimo de 75% - e a pipeline em 88%. O produto está entregue.
