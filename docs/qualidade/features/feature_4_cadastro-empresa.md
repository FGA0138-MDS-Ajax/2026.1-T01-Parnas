# Documentação de Testes - Cadastro de Empresa

---
## 1. Identificação

| Campo | Valor |
|---|---|
| **Feature** | Cadastro de Empresa |
| **Cenário** | CEN-00 |
| **Requisito(s)** | R04 |
| **Branch de desenvolvimento** | `feature/4-cadastro-empresa` |
| **Branch de teste** | `test/feature/4-cadastro-empresa-qa` (recriada a partir da develop) |
| **Sprint(s)** | 4 |
| **Responsáveis** | Daniel Filipe / Matheus Moretti |
| **Data** | 23/05/2026 |

---
## 2. Critérios de aceitação testáveis

> Acordados com a dupla de desenvolvimento no início da feature (US04).

- [x] Usuário consegue cadastrar empresa com nome e CNPJ obrigatórios - `TS-01`, `TS-04`, `TS-05`
- [x] CNPJ duplicado retorna erro com mensagem clara - `TS-02`, `TS-04`, `TS-05` (409 "CNPJ já cadastrado")
- [x] CNPJ é validado (formato e dígitos verificadores) - `TS-01`, `TS-03`
- [x] Após cadastro, usuário é vinculado automaticamente à empresa - `TS-02`, `TS-05`, `TS-06`, `TS-18`

---
## 3. Casos executados

> 60 casos no total (agrupados por arquivo/camada). Detalhe completo nos artifacts da pipeline.

| Caso | Descrição | Nível | Esperado | Observado | Status |
| :--: | --- | --- | --- | --- | :--: |
| TS-01 | Schema: validação de nome/CNPJ/email/telefone (19 casos) | Unitário | aceita válidos, rejeita inválidos/ausentes | Conforme | OK |
| TS-02 | `register_company`: sucesso, CNPJ duplicado (409), erro de BD (500), vínculo (7 casos) | Unitário | status e efeitos corretos | Conforme | OK |
| TS-03 | Validação de CNPJ (formato e dígitos verificadores) (5 casos) | Unitário | rejeita CNPJ inválido | Conforme | OK |
| TS-04 | Rota `POST /api/companies/register`: sucesso, validação, duplicado, content-type, integração (15 casos) | Integração | 201/400/409 conforme cenário | Conforme (1 xfail) | OK |
| TS-05 | Service + BD real: persistência, associação user-company, constraints, rollback, múltiplas empresas (10 casos) | Integração | grava e vincula corretamente | Conforme | OK |
| TS-06 | E2E: fluxo completo cadastro→login→empresa, múltiplos usuários/CNPJs (7 casos) | E2E | fluxo ponta a ponta funciona | Conforme | OK |
| TS-18 | (roteiro) Isolamento/vínculo usuário-empresa | Integração/E2E | cada usuário associado só à sua empresa | Conforme | OK |
| - | Token JWT malformado → deveria 401 | Integração | `401` | `422` (default flask-jwt) | xfail (DEF-01) |

---
## 4. Evidências

> Resultados conferem com os artifacts da pipeline (GitHub Actions, `tests.yml`):
> `tests.unit.feature_4`, `tests.integration.feature_4` e `tests.e2e.feature_4`
> somam **60 casos - 59 pass, 0 fail, 1 xfail**.

### Backend - `python -m pytest tests/unit/feature_4 tests/integration/feature_4 tests/e2e/feature_4 -q`

```
tests/unit/feature_4/test_company_schema.py ................        (19)
tests/unit/feature_4/test_company_service.py .......               (7)
tests/unit/feature_4/test_company_validators.py .....              (5)
tests/integration/feature_4/test_company_routes.py .x.............  (15, 1 xfail)
tests/integration/feature_4/test_company_service_db.py ..........   (10)
tests/e2e/feature_4/test_company_registration_flow.py .......       (7)

================== 59 passed, 1 xfailed in ~17s ==================
```

> **Nota de organização (QA):** os testes do Matheus estavam espalhados (arquivos
> soltos + duplicados) e com 11 falhas de **teste/ambiente** (mocks que patchavam
> a classe `Company` inteira, CNPJs de teste inválidos, expectativa errada de
> campos extras). Foram **reorganizados** em `tests/{unit,integration,e2e}/feature_4/`
> e as falhas corrigidas no lado do teste - **nenhuma era bug do código de produção**
> de company. Guias/rascunhos e artefatos versionados foram removidos.

---
## 5. Defeitos encontrados

| Issue | Descrição | Status |
|---|---|---|
| DEF-01 | Token JWT malformado retorna **HTTP 422** (default do flask-jwt-extended), não **401** como o contrato espera. Exige um handler customizado de erro de token (`@jwt.invalid_token_loader`). Marcado `xfail`. Branch sugerida: `fix/jwt-erro-401`. | Aberto |

> Nenhum defeito de produção encontrado no fluxo de **cadastro de empresa**
> (criar, CNPJ duplicado, validação de CNPJ, vínculo automático) - todos os
> critérios passam.

---
## 6. Cobertura

```bash
pytest tests/unit/feature_4 tests/integration/feature_4 tests/e2e/feature_4 \
  --cov=app.services.company_service --cov=app.routes.company_routes \
  --cov=app.schemas.company_schema --cov=app.utils.validators --cov-report=term-missing
```

| Métrica | Valor |
|---|---|
| `app/schemas/company_schema.py` | 88% |
| `app/routes/company_routes.py` | 55% (rota de registro coberta; `delete`/`update` fora do escopo) |
| `app/services/company_service.py` | 42% (`register_company` coberto; `delete`/`update`/`find` fora do escopo) |
| `app/utils/validators.py` | 15% (só a validação de **CNPJ** é desta feature; o resto são validadores de usuário/senha) |
| **TOTAL (recorte por módulo)** | **49%** |

> A cobertura por módulo fica **abaixo da meta de 60%** porque esses módulos
> contêm muito código de **outras features** (exclusão/edição de empresa,
> validadores de usuário). O **caminho de cadastro de empresa em si** (schema,
> `register_company`, rota de registro e validação de CNPJ) está bem exercitado.
> Critério da issue "Cobertura mínima atingida" permanece `[ ]`.

---
## 7. Parecer final

> **Status:** Aprovada com pendências.
>
> Os **4 critérios de aceitação** estão cobertos e verdes (**59/60**, com 1 `xfail`
> documentado), nas três camadas (unit, integração e E2E): cadastro com nome/CNPJ
> obrigatórios, erro claro de CNPJ duplicado (409), validação de dígitos do CNPJ e
> vínculo automático usuário↔empresa. Nenhum defeito de produção foi encontrado no
> fluxo de cadastro.
>
> **Pendências (não bloqueantes):**
> 1. **DEF-01** - padronizar o retorno de token JWT inválido para `401` (hoje `422`); depois remover o `xfail`.
> 2. **Cobertura mínima** - o número por módulo (49%) está abaixo de 60% por diluição com código de outras features; se a meta for por módulo, completar testes de `delete`/`update` de empresa (fora do escopo desta US) ou medir a cobertura só do recorte da feature.
