# Documentação de Testes — Template de Feature

> Copie este arquivo para `qualidade/features/<nome-da-feature>.md` e preencha os
> campos. Remova os trechos de instrução (entre `>`) ao finalizar.
 ---
## 1. Identificação

| Campo | Valor |
| --- | --- |
| **Feature** | *Nome da feature* |
| **Cenário** | *CEN-0X* |
| **Requisito(s)** | *R0X* |
| **Branch de desenvolvimento** | `feature/<nome>` |
| **Branch de teste** | `test/feature/<numero-nome>` |
| **Sprint(s)** | *N* |
| **Responsáveis** | Daniel Filipe / Matheus Moretti |
| **Data** | *dd/mm/aaaa* |
 ---
## 2. Critérios de aceitação testáveis

> Acordados com a dupla de desenvolvimento no início da feature.

- [ ] Critério 1
- [ ] Critério 2

---
## 3. Casos executados

| Caso | Descrição | Nível | Esperado | Observado | Status |
| :--: | --- | --- | --- | --- | :--: |
| TS-0X | *...* | Unitário | *...* | *...* | ✅ / ❌ |

---
## 4. Evidências

> Trechos de código de teste, saídas de `pytest`, prints. Exemplo:

```bash
pytest tests/unit/test_company_service.py -v
```

```
tests/unit/test_company_service.py::test_register_company_success PASSED
tests/unit/test_company_service.py::test_register_company_duplicate_cnpj PASSED
```

---
## 5. Defeitos encontrados

| Issue | Descrição | Branch de correção | Status |
| --- | --- | --- | --- |
| #— | *...* | `fix/<nome>` | Aberto / Corrigido |

---
## 6. Cobertura

```bash
pytest --cov=app tests/
```

| Métrica | Valor |
| --- | --- |
| Cobertura da feature | *—%* |

---
## 7. Parecer final

> **Status:** Aprovada / Aprovada com pendências / Reprovada
>
> *Justificativa e próximos passos.*

---