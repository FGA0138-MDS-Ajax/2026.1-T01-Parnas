# Consolidado de Testes e GQM - Sprint 5

| Campo | Valor |
|---|---|
| **Sprint** | 5 |
| **Período** | 24-30/mai |
| **Foco** | Conclusão da autenticação e categorização financeira (CEN-00, Func. A e B) |

---
## 1. Features testadas

| Feature | Requisito | Status |
| --- | :--: | --- |
| [Recuperação de senha](../features/feature_3_recuperacao-senha.md) | R05 | Aprovada |
| [Exclusão de usuário/empresa](../features/feature_8_exclusao-usuario-empresa.md) | R02 | Aprovada |
| [Cadastro de categoria](../features/feature_5_cadastro-categoria.md) | R06 | Aprovada |

---
## 2. Casos agregados

| Caso | Nível | Status |
| :--: | --- | :--: |
| TS-13 | Integração | OK |
| TS-14 | Integração | OK |
| TS-15 | Integração | OK |

## 3. Defeitos

| # | Descrição | Branch | Status |
| :--: | --- | --- | --- |
| 1 | Testes de Cadastro de Empresa com mocks/asserts desatualizados | `fix/testes-empresa` | Corrigido |
| 2 | Exclusão de conta não invalida a sessão ativa | `fix/exclusao-conta-sessao` | Em aberto (S10) |

## 4. Números gerais

| Indicador | Valor |
| --- | :--: |
| Casos planejados | 3 |
| Casos executados | 3 |
| Casos aprovados | 3 |
| Defeitos encontrados | 2 |

## 5. Cobertura (M3)

```bash
pytest --cov=app tests/
```

| Cobertura | Valor | Mínimo (S1-5) |
| --- | :--: | :--: |
| Back-end | 69% | 60% |
| Front-end | 67% (Vitest) | 60% |
| M3 (média back + front) | 68% | 60% |

## 6. Análise GQM

| Métrica | Valor | Meta |
| :--: | :--: | --- |
| M1 - Throughput | 6 issues | Tendência estável/crescente |
| M2 - Densidade de Defeitos | 0,33 | ≈ 0 |
| M3 - Cobertura | 68% (back 69% / front 67%) | ≥ 60% |
| M4 - Taxa de Aprovação da Pipeline | 67% | ≥ 70% (a partir da S5) |

## 7. Parecer da dupla

> A Sprint fechou o cenário CEN-00 (recuperação de senha e exclusão com cascata) e
> iniciou o CEN-01 com a categorização. Throughput subiu para 6 issues e a densidade
> de defeitos caiu para 0,33. A pipeline ficou ligeiramente abaixo da meta (67%);
> a recomendação para a S6 é rodar a suíte localmente antes de cada PR. O defeito de
> invalidação de sessão foi mapeado para a estabilização.
