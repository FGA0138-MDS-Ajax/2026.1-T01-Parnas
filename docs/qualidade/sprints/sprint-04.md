# Consolidado de Testes e GQM - Sprint 4

| Campo | Valor |
|---|---|
| **Sprint** | 4 |
| **Período** | 17-23/mai |
| **Foco** | Plataforma e autenticação - cadastro, login e empresa (CEN-00, Func. A parcial) |

---
## 1. Features testadas

| Feature | Requisito | Status |
| --- | :--: | --- |
| [Cadastro de usuário](../features/feature_1_cadastro-usuario.md) | R01 | Aprovada com pendências |
| [Autenticação e login](../features/feature_2_autenticacao-login.md) | R03 | Aprovada com pendências |
| [Cadastro de empresa](../features/feature_4_cadastro-empresa.md) | R04 | Aprovada com pendências |

---
## 2. Casos agregados

| Caso | Nível | Status |
| :--: | --- | :--: |
| TS-01 | Unitário | OK |
| TS-02 | Unitário | OK |
| TS-03 | Unitário | OK |
| TS-04 | Unitário | OK |
| TS-12 | Integração | OK |
| TS-18 | Integração | OK |

## 3. Defeitos

| # | Descrição | Branch | Status |
| :--: | --- | --- | --- |
| 1 | `is_valid_password` aceita senha com espaços (deveria rejeitar) | `fix/validador-senha` | Corrigido na S10 |
| 2 | `Register.jsx` não preenche estado de Nome/Senha (caminho feliz bloqueado) | `fix/cadastro-estado` | Corrigido na S10 |

## 4. Números gerais

| Indicador | Valor |
| --- | :--: |
| Casos planejados | 6 |
| Casos executados | 6 |
| Casos aprovados | 6 |
| Defeitos encontrados | 2 |

## 5. Cobertura (M3)

```bash
pytest --cov=app tests/
```

| Cobertura | Valor | Mínimo (S1-5) |
| --- | :--: | :--: |
| Back-end | 63% | 60% |
| Front-end | 62% (Vitest) | 60% |
| M3 (média back + front) | 63% | 60% |

## 6. Análise GQM

| Métrica | Valor | Meta |
| :--: | :--: | --- |
| M1 - Throughput | 5 issues | Tendência estável/crescente |
| M2 - Densidade de Defeitos | 0,40 | ≈ 0 |
| M3 - Cobertura | 63% (back 63% / front 62%) | ≥ 60% |
| M4 - Taxa de Aprovação da Pipeline | - (CI em implantação) | ≥ 70% (a partir da S5) |

## 7. Parecer da dupla

> Primeira Sprint de construção: a base de autenticação foi entregue e validada no
> núcleo de negócio (cadastro, login e empresa). A densidade de defeitos (0,40)
> reflete a maturidade inicial das práticas de teste - os dois defeitos de cadastro
> foram registrados como `bug` e encaminhados para a Sprint de estabilização. A
> pipeline de CI de testes ainda estava em implantação, então M4 não foi medida.
