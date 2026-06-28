# Documentação de Testes - Centralização Documental

---
## 1. Identificação

| Campo                         | Valor                                     |
|-------------------------------|-------------------------------------------|
| **Feature**                   | Centralização Documental                  |
| **Cenário**                   | CEN-02                                    |
| **Requisito(s)**              | R10                                       |
| **Branch de desenvolvimento** | `feature/9-centralizacao-documental`      |
| **Branch de teste**           | `test/feature/9-centralizacao-documental` |
| **Sprint(s)**                 | 8                                         |
| **Responsáveis**              | Daniel Filipe / Matheus Moretti           |
| **Data**                      | 16/06/2026                                |

---
## 2. Critérios de aceitação testáveis

> Acordados com a dupla de desenvolvimento no início da feature (US09).

- [x] Gestor consegue enviar documento informando nome, tipo e descrição - `TS-01`, `TS-24`
- [x] Sistema valida tipo e tamanho do arquivo enviado - `TS-03`, `TS-04`, `TS-11`-`TS-15`, `TS-21`, `TS-22`
- [ ] Documentos são listados com nome, tipo, data e tamanho - `TS-08`: **falha** (HTTP 500) → **DEF-01**
- [ ] Gestor consegue baixar um documento enviado - `TS-09`: **falha** (HTTP 500) → **DEF-03**
- [ ] Gestor consegue excluir um documento com confirmação - backend `TS-10`: **falha** (404 indevido) → **DEF-02**; front (mock) `TS-25`/`TS-26` OK
- [x] Documentos são exclusivos por empresa - outra empresa não os vê - `TS-07` (acesso negado com `403`); a checagem de listagem por empresa fica bloqueada pelo DEF-01

> **Rastreabilidade do roteiro:** `TS-19` (upload e organização de documentos) → coberto por `TS-01` (upload via API) e `TS-20`/`TS-24` (front).
> **Nota de ambiente:** o `conftest.py` passou a vincular `test_user` ↔ `test_company` (tabela `user_company`), pois os services de documento/transação exigem esse vínculo (403 caso contrário).

---
## 3. Casos executados

| Caso   | Descrição                                             | Nível            | Esperado                      | Observado                           |     Status     |
|:------:|-------------------------------------------------------|------------------|-------------------------------|-------------------------------------|:--------------:|
| TS-01  | `POST /api/documentos` com arquivo válido (multipart) | Integração       | `201` + documento             | Conforme                            |       OK       |
| TS-02  | `POST` sem campo `file`                               | Integração       | `400`                         | Conforme                            |       OK       |
| TS-03  | `POST` com extensão não permitida (`.exe`)            | Integração       | `400`                         | Conforme                            |       OK       |
| TS-04  | `POST` com tipo fora de fiscal/contabil/juridico      | Integração       | `400` (validação)             | Conforme                            |       OK       |
| TS-05  | `POST` sem nome                                       | Integração       | `400` (validação)             | Conforme                            |       OK       |
| TS-06  | `POST` sem token                                      | Integração       | `401`                         | Conforme                            |       OK       |
| TS-07  | `POST` em empresa sem vínculo do usuário              | Integração       | `403`                         | Conforme                            |       OK       |
| TS-08  | `GET /api/documentos` lista os documentos da empresa  | Integração       | `200` + lista                 | `500` (`tipo` kwarg)                | xfail (DEF-01) |
| TS-09  | `GET /api/documentos/<id>/download`                   | Integração       | `200` + arquivo               | `500` (`get_by_id` inexistente)     | xfail (DEF-03) |
| TS-10  | `DELETE /api/documentos/<id>`                         | Integração       | `200`                         | `404` (busca com `company_id=None`) | xfail (DEF-02) |
| TS-11  | `validate_file_extension` com extensão permitida      | Unitário         | `True`                        | Conforme                            |       OK       |
| TS-12  | `validate_file_extension` com extensão não permitida  | Unitário         | `False`                       | Conforme                            |       OK       |
| TS-13  | `validate_file_extension` sem extensão                | Unitário         | `False`                       | Conforme                            |       OK       |
| TS-14  | `validate_file_size` dentro do limite                 | Unitário         | `True`                        | Conforme                            |       OK       |
| TS-15  | `validate_file_size` acima do limite                  | Unitário         | `False`                       | Conforme                            |       OK       |
| TS-16  | `check_user_company_access` usuário inexistente       | Unitário         | `404`                         | Conforme                            |       OK       |
| TS-17  | `check_user_company_access` empresa inexistente       | Unitário         | `404`                         | Conforme                            |       OK       |
| TS-18  | `check_user_company_access` sem vínculo               | Unitário         | `403`                         | Conforme                            |       OK       |
| TS-19  | `check_user_company_access` com vínculo               | Unitário         | acesso liberado               | Conforme                            |       OK       |
| TS-20  | Página inicia sem documentos                          | Unitário (front) | "Nenhum documento cadastrado" | Conforme                            |       OK       |
| TS-21  | Arquivo de tipo inválido mostra erro                  | Unitário (front) | mensagem de erro              | Conforme                            |       OK       |
| TS-22  | Arquivo acima de 5MB mostra erro                      | Unitário (front) | mensagem de erro              | Conforme                            |       OK       |
| TS-23  | Submeter sem arquivo mostra erro                      | Unitário (front) | "Selecione um arquivo"        | Conforme                            |       OK       |
| TS-24  | Upload válido adiciona documento na tabela            | Unitário (front) | documento listado             | Conforme                            |       OK       |
| TS-25  | Excluir documento com confirmação                     | Unitário (front) | removido da tabela            | Conforme                            |       OK       |
| TS-26  | Cancelar exclusão mantém o documento                  | Unitário (front) | documento permanece           | Conforme                            |       OK       |

---
## 4. Evidências

> Os resultados batem com os artifacts da pipeline (GitHub Actions, `tests.yml`):
> `testes/relatorio-backend/test-results.xml` já inclui `tests.unit.feature_9` e
> `tests.integration.feature_9` (16 pass, 0 fail, 3 xfail).

### Backend - `python -m pytest tests/unit/feature_9 tests/integration/feature_9 -q`

```
tests/unit/feature_9/test_document_service.py .........
tests/integration/feature_9/test_document_endpoints.py .......xxx

================== 16 passed, 3 xfailed in 4.15s ==================
```

Os 3 `xfail` (defeitos documentados):
```
TS-08  test_lista_documentos_da_empresa   -> DEF-01 (500)
TS-09  test_download_documento            -> DEF-03 (500)
TS-10  test_exclui_documento              -> DEF-02 (404 indevido)
```

### Frontend - `npm run test:run -- src/pages/Documentos/Documentos.test.jsx`

```
 src/pages/Documentos/Documentos.test.jsx (7 tests)
 Test Files  1 passed (1)
      Tests  7 passed (7)
```

**Total:** 26 testes - **23 passaram**, **3 xfail** (defeitos documentados), 0 falha inesperada.

---
## 5. Defeitos encontrados

> Defeitos no código da `feature/9` (ainda não mergeada na develop) - devem ser
> corrigidos na própria branch de desenvolvimento antes do PR `feature/9 → develop`.

| Issue               | Descrição                                                                                                                                                                                                                                                                                                                                                                                  | Status |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| DEF-01              | **Listagem quebrada.** A rota `GET /api/documentos` chama `DocumentService.get_documents_by_company(..., tipo=...)`, mas a assinatura do service **não tem o parâmetro `tipo`** → `TypeError`/HTTP 500. Critério "documentos listados" não funciona. Branch sugerida: `fix/documentos-listagem-tipo`.                                                                                      | Aberto |
| DEF-02              | **Exclusão quebrada.** `delete_document` chama `DocumentRepository.get_by_id_and_company(document_id, None)` com `company_id=None`; o filtro nunca casa → retorna **404 mesmo para documento existente**. Branch sugerida: `fix/documentos-delete-company-id`.                                                                                                                             | Aberto |
| DEF-03              | **Download quebrado.** `get_document_for_download` chama `DocumentRepository.get_by_id(...)`, método **inexistente** no repository → `AttributeError`/HTTP 500. Branch sugerida: `fix/documentos-download-get-by-id`.                                                                                                                                                                      | Aberto |
| DEF-04 (observação) | **Divergência front↔back e front não integrado.** O front (`Documentos.jsx`) valida PDF/PNG/JPG e 5 MB, com tipos "Contrato/Comprovante/Declaração/Relatório"; o backend aceita `pdf/txt/md`, 50 MB e tipos `fiscal/contabil/juridico`. Além disso o front opera sobre estado local (tarefa "Integrar todos os endpoints" em aberto). Branch sugerida: `fix/documentos-alinha-front-back`. | Aberto |

---
## 6. Cobertura

```bash
# Backend
pytest tests/unit/feature_9 tests/integration/feature_9 \
  --cov=app.services.document_service --cov=app.routes.document_routes \
  --cov=app.schemas.document_schema --cov=app.models.document \
  --cov=app.repositories.document_repository --cov-report=term-missing

# Frontend
npm run test:run -- src/pages/Documentos/Documentos.test.jsx --coverage
```

| Métrica                                       |  Valor                                                                                          |
|-----------------------------------------------|-------------------------------------------------------------------------------------------------|
| `app/schemas/document_schema.py`              | 100%                                                                                            |
| `app/models/document.py`                      | 94%                                                                                             |
| `app/routes/document_routes.py`               | 86%                                                                                             |
| `app/repositories/document_repository.py`     | 80%                                                                                             |
| `app/services/document_service.py`            | 71% (não-coberto: ramos de download/listagem/exclusão barrados pelos DEFs + tratamento de erro) |
| **Backend - total (módulos importados)**      | **79%**                                                                                         |
| `src/pages/Documentos/Documentos.jsx` (front) | 88%                                                                                             |

Cobertura acima da meta de **≥ 60%**; o não-coberto do service concentra-se justamente nos caminhos quebrados (DEF-01/02/03).

---
## 7. Parecer final

> **Status:** Aprovada com pendências.
>
> O **upload** e todas as **validações** (extensão, tamanho, tipo, nome, vínculo
> usuário↔empresa) estão corretos e cobertos (23/26 verdes, cobertura **79%**).
> Restam **3 critérios de aceitação** bloqueados por defeitos de integração no
> backend - **listar** (DEF-01), **baixar** (DEF-03) e **excluir** (DEF-02) - que
> ficam registrados como **pendências** a serem corrigidas na `feature/9` antes do
> merge na develop.
>
> Os três defeitos são **pequenos e localizados** (um kwarg a mais, um argumento
> `None` e um método ausente no repository) - uma correção rápida na `feature/9`
> seguida de novo run deve tornar `TS-08/09/10` verdes e encerrar as pendências
> (restando o alinhamento do DEF-04).
>
> **Próximos passos (pendências):**
> 1. **DEF-01** - remover/implementar o filtro `tipo` em `get_documents_by_company`.
> 2. **DEF-02** - buscar o documento por id (sem `company_id=None`) antes de checar acesso.
> 3. **DEF-03** - adicionar `get_by_id` ao `DocumentRepository` (ou usar o método correto).
> 4. **DEF-04** - alinhar validações front↔back e integrar o front aos endpoints.
> 5. Reexecutar a suíte da feature 9 e atualizar este documento.

---
