# Consolidado de Testes e GQM - Sprint 6

| Campo       | Valor                                                               |
|-------------|---------------------------------------------------------------------|
| **Sprint**  | 6                                                                   |
| **Período** | 31/mai-06/jun                                                       |
| **Foco**    | Registro de transações e histórico financeiro (CEN-01, Func. C e D) |

---
## 1. Features testadas

| Feature                                                                  | Requisito   | Status                  |
|--------------------------------------------------------------------------|:-----------:|-------------------------|
| [Cadastro de transação](../features/feature_6_cadastro-transacao.md)     |     R07     | Aprovada com pendências |
| [Histórico de transações](../features/feature_7_historico-transacoes.md) |     R08     | Reprovada               |

---
## 2. Casos agregados

| Caso   | Nível      | Status   |
|:------:|------------|:--------:|
| TS-05  | Unitário   |    OK    |
| TS-11  | Unitário   |    OK    |
| TS-16  | Integração |    OK    |
| TS-17  | Integração |  Falhou  |
| TS-25  | Sistema    | Pendente |

## 3. Defeitos

| #   | Descrição                                                      | Branch                      | Status          |
|:---:|----------------------------------------------------------------|-----------------------------|-----------------|
|  1  | Cálculo de totais do histórico com mistura `Decimal`/`float`   | `fix/totais-historico`      | Corrigido       |
|  2  | Aba de Transações exibindo dados mock em vez de consumir a API | `fix/integracao-transacoes` | Em aberto (S10) |

## 4. Números gerais

| Indicador            |  Valor |
|----------------------|:------:|
| Casos planejados     |   5    |
| Casos executados     |   5    |
| Casos aprovados      |   3    |
| Defeitos encontrados |   2    |

## 5. Cobertura (M3)

```bash
pytest --cov=app tests/
```

| Cobertura               |    Valor     | Mínimo (S6-10) |
|-------------------------|:------------:|:--------------:|
| Back-end                |     73%      |      75%       |
| Front-end               | 78% (Vitest) |      75%       |
| M3 (média back + front) |     76%      |      75%       |

## 6. Análise GQM

|             Métrica                |          Valor             |  Meta                       |
|:----------------------------------:|:--------------------------:|-----------------------------|
|          M1 - Throughput           |          6 issues          | Tendência estável/crescente |
|     M2 - Densidade de Defeitos     |            0,33            | ≈ 0                         |
|           M3 - Cobertura           | 76% (back 73% / front 78%) | ≥ 75%                       |
| M4 - Taxa de Aprovação da Pipeline |            72%             | ≥ 70%                       |

## 7. Parecer da dupla

> O cadastro de transação foi aprovado, mas o histórico foi **reprovado**: o cálculo
> de totais com filtros divergiu por mistura de `Decimal`/`float` e a tela ainda
> consumia dados mock. Ambos os defeitos foram registrados como `bug` e encaminhados.
> Com a cobertura de front-end (78%) somada à de back-end (73%), o M3 médio chegou a
> 76%, acima do novo mínimo de 75%. A pipeline superou a meta (72%).
