# Documentação de Testes - Seleção de Empresa Ativa

---
## 1. Identificação

| Campo | Valor |
|---|---|
| **Feature** | Seleção de Empresa Ativa |
| **Cenário** | CEN-00 |
| **Requisito(s)** | R04 |
| **Branch de desenvolvimento** | `feature/15-selecao-empresa-ativa` |
| **Branch de teste** | `feature/15-selecao-empresa-ativa` (testes de QA commitados na própria branch) |
| **PR** | #76 (para `develop`) |
| **Sprint(s)** | 7 |
| **Responsáveis** | Daniel Filipe / Matheus Moretti |
| **Data** | 27/06/2026 |

---
## 2. Critérios de aceitação testáveis

> Acordados com a dupla de desenvolvimento no início da feature.

- [x] `GET /api/usuarios/me/empresas` lista as empresas vinculadas ao usuário logado
- [x] `POST /api/sessao/empresa-ativa` define a empresa ativa e devolve um novo JWT
- [x] Selecionar empresa sem vínculo é bloqueado (403)
- [x] `company_id` é obrigatório ao definir a empresa ativa (400)
- [x] Frontend: contexto de empresa e tela de seleção cobertos por Vitest

---
## 3. Casos executados

Backend: `tests/integration/feature_15/test_session.py`. Frontend: suíte Vitest da branch.

| Caso | Descrição | Nível | Esperado | Observado | Status |
| :--: | --- | --- | --- | --- | :--: |
| QA-01 | Listar empresas sem token | Integração | 401 | 401 | Passou |
| QA-02 | Listar empresas do usuário | Integração | 200 + empresa vinculada | 200 | Passou |
| QA-03 | Definir empresa ativa sem `company_id` | Integração | 400 | 400 | Passou |
| QA-04 | Definir empresa sem vínculo | Integração | 403 | 403 | Passou |
| QA-05 | Definir empresa ativa válida | Integração | 200 + token + `active_company_id` | 200 | Passou |
| QA-F | `EmpresaContext` / `SelecaoEmpresa` / `Login` (Vitest) | Front | suíte verde | 98 testes verdes | Passou |

---
## 4. Evidências

```bash
python -m pytest tests/integration/feature_15 -q
# 5 passed

npm run test:run   # frontend
# Test Files 20 passed (20) | Tests 98 passed (98)
```

---
## 5. Defeitos encontrados

| Issue | Descrição | Status |
|---|---|---|
| PEND-1 | A branch está 7 commits à frente da `develop` e refatorou vários services; a suíte de backend da branch acusa **99 testes falhando** (feature_4, 5, 6, 7, 9, 10, 11, 12, 14). São testes desatualizados frente aos refactors (mesma natureza da task7/fix3), não defeitos da feature de seleção de empresa. | Aberto |

---
## 6. Cobertura

| Métrica | Valor |
|---|---|
| Cobertura da feature | Endpoints de sessão (lista + empresa ativa) cobertos; frontend coberto |

---
## 7. Parecer final

> **Status:** Aprovada com pendências
>
> A feature de seleção de empresa ativa funciona nas duas camadas: os endpoints de sessão
> passam (5/5) e o frontend (contexto + tela de seleção) está verde (98 testes). A
> pendência é a suíte de backend da branch, que carrega 99 falhas herdadas dos refactors
> de services - testes desatualizados que precisam ser reconciliados (junto com a task7)
> antes do merge na `develop`. Não é defeito da feature em si.
