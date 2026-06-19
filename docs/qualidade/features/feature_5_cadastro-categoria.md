# Documentação de Testes - Cadastro de Categoria

---
## 1. Identificação

| Campo                         | Valor                               |
|-------------------------------|-------------------------------------|
| **Feature**                   | Cadastro de Categoria               |
| **Cenário**                   | CEN-01                              |
| **Requisito(s)**              | R06                                 |
| **Branch de desenvolvimento** | `feature/5-cadastro-categoria`      |
| **Branch de teste**           | `test/feature/5-cadastro-categoria` |
| **Sprint(s)**                 | 5                                   |
| **Responsáveis**              | Daniel Filipe / Matheus Moretti     |
| **Data**                      | 25/05/2026                          |

---
## 2. Critérios de aceitação testáveis

> Acordados com a dupla de desenvolvimento no início da feature (issue #16).

- [x] Gestor consegue criar uma categoria com nome e tipo (receita/despesa) - `TS-01`, `TS-15`, `TS-20`
- [x] Categorias são exclusivas por empresa - outra empresa não as vê - `TS-06`
- [x] Não é possível criar duas categorias com o mesmo nome na mesma empresa - `TS-10` (bloqueio funcional via constraint `UNIQUE`); porém retorna **HTTP 500** em vez de erro tratado → ver **DEF-01**
- [x] Gestor consegue listar todas as categorias da sua empresa - `TS-05`, `TS-19`
- [x] Gestor consegue editar o nome de uma categoria existente - `TS-07`, `TS-22`
- [ ] Gestor consegue excluir uma categoria que **não** tenha transações vinculadas - exclusão simples funciona (`TS-09`, `TS-24`), mas o **bloqueio** quando há transações vinculadas **não está implementado** (`TS-12`) → ver **DEF-02**
- [ ] (implícito) Operação restrita à empresa do usuário autenticado - `TS-13`: o `user_id` do JWT é ignorado → ver **DEF-03**

---
## 3. Casos executados

| Caso  | Descrição                                                   | Nível            | Esperado                         | Observado                          |      Status       |
|:-----:|-------------------------------------------------------------|------------------|----------------------------------|------------------------------------|:-----------------:|
| TS-01 | `POST /api/categories` com dados válidos                    | Integração       | `201` + mensagem de sucesso      | Conforme                           |         OK         |
| TS-02 | `POST /api/categories` sem token                            | Integração       | `401`                            | Conforme                           |         OK         |
| TS-03 | `POST` com CNPJ válido de empresa não cadastrada            | Integração       | `404` + "Empresa não encontrada" | Conforme                           |         OK         |
| TS-04 | `POST` com CNPJ fora de formato                             | Integração       | `400` (barrado pelo schema)      | Conforme                           |         OK         |
| TS-05 | `GET /api/categories?cnpj=` lista categorias da empresa     | Integração       | só as categorias daquela empresa | Conforme                           |         OK         |
| TS-06 | Listagem não inclui categorias de outra empresa             | Integração       | categoria da empresa B ausente   | Conforme                           |         OK         |
| TS-07 | `PUT /api/categories` edita o nome de categoria existente   | Integração       | `200` + nome atualizado          | Conforme                           |         OK         |
| TS-08 | `PUT` em categoria inexistente                              | Integração       | `404`                            | Conforme                           |         OK         |
| TS-09 | `DELETE /api/categories` de categoria sem transações        | Integração       | `200` + some da listagem         | Conforme                           |         OK         |
| TS-10 | Nome duplicado na mesma empresa não cria 2ª categoria       | Integração       | duplicata bloqueada (1 registro) | Bloqueada pela constraint `UNIQUE` |         OK         |
| TS-11 | Nome duplicado retorna status amigável (400/409)            | Integração       | `400` ou `409`                   | `500` (IntegrityError vazado)      | xfail (DEF-01) |
| TS-12 | Exclusão de categoria com transações vinculadas é bloqueada | Integração       | `400`/`409` recusando a exclusão | Exclusão não é bloqueada           | xfail (DEF-02) |
| TS-13 | Usuário sem vínculo não gerencia categoria de outra empresa | Integração       | `403`                            | `201` - `user_id` ignorado         | xfail (DEF-03) |
| TS-14 | `add_category` com empresa inexistente                      | Unitário         | `404`                            | Conforme                           |         OK         |
| TS-15 | `add_category` com empresa válida persiste a categoria      | Unitário         | `201` + `db.session.add/commit`  | Conforme                           |         OK         |
| TS-16 | `get_categories` com empresa inexistente                    | Unitário         | `404`                            | Conforme                           |         OK         |
| TS-17 | `update_category` com categoria inexistente                 | Unitário         | `404`                            | Conforme                           |         OK         |
| TS-18 | `delete_category` com categoria inexistente                 | Unitário         | `404`                            | Conforme                           |         OK         |
| TS-19 | Página lista as categorias iniciais                         | Unitário (front) | Salário e Alimentação na tela    | Conforme                           |         OK         |
| TS-20 | Adicionar nova categoria pelo formulário                    | Unitário (front) | nova categoria aparece na tabela | Conforme                           |         OK         |
| TS-21 | Formulário limpa o nome após adicionar                      | Unitário (front) | campo de nome volta a vazio      | Conforme                           |         OK         |
| TS-22 | Editar nome de categoria inline                             | Unitário (front) | nome trocado, antigo some        | Conforme                           |         OK         |
| TS-23 | Cancelar edição mantém o nome original                      | Unitário (front) | nome original preservado         | Conforme                           |         OK         |
| TS-24 | Excluir categoria após confirmação                          | Unitário (front) | categoria removida da tabela     | Conforme                           |         OK         |
| TS-25 | Não excluir quando a confirmação é cancelada                | Unitário (front) | categoria permanece              | Conforme                           |         OK         |

---
## 4. Evidências

> Os resultados batem com os artifacts da pipeline (GitHub Actions, workflow `tests.yml`):
> `testes/relatorio-backend/test-results.xml` e `coverage.xml` já incluem
> `tests.unit.feature_5` e `tests.integration.feature_5`.

### Backend - `python -m pytest tests/unit/feature_5 tests/integration/feature_5 -v`

```
tests/unit/feature_5/test_category_service.py::test_add_category_empresa_inexistente PASSED
tests/unit/feature_5/test_category_service.py::test_add_category_empresa_valida PASSED
tests/unit/feature_5/test_category_service.py::test_get_categories_empresa_inexistente PASSED
tests/unit/feature_5/test_category_service.py::test_update_category_inexistente PASSED
tests/unit/feature_5/test_category_service.py::test_delete_category_inexistente PASSED
tests/integration/feature_5/test_category_endpoints.py::test_cria_categoria_dados_validos PASSED
tests/integration/feature_5/test_category_endpoints.py::test_cria_categoria_sem_token PASSED
tests/integration/feature_5/test_category_endpoints.py::test_cria_categoria_empresa_inexistente PASSED
tests/integration/feature_5/test_category_endpoints.py::test_cria_categoria_cnpj_invalido PASSED
tests/integration/feature_5/test_category_endpoints.py::test_lista_categorias_da_empresa PASSED
tests/integration/feature_5/test_category_endpoints.py::test_lista_categorias_nao_inclui_de_outra_empresa PASSED
tests/integration/feature_5/test_category_endpoints.py::test_atualiza_nome_categoria PASSED
tests/integration/feature_5/test_category_endpoints.py::test_atualiza_categoria_inexistente PASSED
tests/integration/feature_5/test_category_endpoints.py::test_exclui_categoria_sem_transacoes PASSED
tests/integration/feature_5/test_category_endpoints.py::test_nome_duplicado_nao_permite_segunda PASSED
tests/integration/feature_5/test_category_endpoints.py::test_nome_duplicado_retorna_status_amigavel XFAIL
tests/integration/feature_5/test_category_endpoints.py::test_exclui_categoria_com_transacoes_e_bloqueado XFAIL
tests/integration/feature_5/test_category_endpoints.py::test_usuario_sem_vinculo_nao_gerencia_categoria_de_outra_empresa XFAIL

================== 15 passed, 3 xfailed in 4.93s ==================
```

> Os 3 `xfail` documentam **DEF-01/02/03** - defeitos conhecidos e tolerados nesta
> entrega; mantêm a suíte verde sem esconder o problema.

### Frontend - `npx vitest run src/pages/Categorias/Categorias.test.jsx`

```
 src/pages/Categorias/Categorias.test.jsx (7 tests)
 Test Files  1 passed (1)
      Tests  7 passed (7)
```

**Total:** 25 testes - **22 passaram**, **3 xfail** (defeitos documentados), 0 falha inesperada.

---
## 5. Defeitos encontrados

> Os defeitos abaixo eram **esperados** nesta entrega e **não reprovam** a feature
> (ver §7). Estão alinhados às issues de correção/refatoração já abertas: **#49**
> (Fix I - bugs front/back), **#56** (Fix III - integração entre classes) e **#35**
> (Tarefa V - Refatoração: DTOs no backend e redesign do frontend).

| Issue | Descrição | Status |
|---|---|---|
| DEF-01 (→ #49) | `add_category` não valida duplicidade antes de gravar; o `IntegrityError` da constraint `UNIQUE(name, company_id)` é capturado pelo `except` genérico e vira **HTTP 500** em vez de `400/409`. Bloqueio funciona, status está errado. Branch sugerida: `fix/categoria-duplicada-status`. | Aberto |
| DEF-02 (→ #49) | `delete_category` **não bloqueia** exclusão de categoria com transações vinculadas (FK `RESTRICT` não honrado no SQLite e sem checagem no service). Corresponde à tarefa em aberto na issue #16. Branch sugerida: `fix/categoria-bloqueio-exclusao`. | Aberto |
| DEF-03 (→ #56) | Service ignora o `user_id` do JWT: qualquer usuário autenticado gerencia categorias de **qualquer empresa** pelo CNPJ, sem checar o vínculo `user_company` (N:N). **Falha de autorização** - prioridade. Branch sugerida: `fix/categoria-autorizacao-empresa`. | Aberto |
| DEF-04 (→ #35) | `app/repositories/category_repository.py` é **código morto** (cobertura 0%, nunca importado); o service consulta os models direto. Candidato à refatoração. Branch sugerida: `refactor/categoria-usa-repository`. | Aberto |

---
## 6. Cobertura

```bash
# Backend
pytest tests/unit/feature_5 tests/integration/feature_5 \
  --cov=app.services.category_service --cov=app.routes.category_routes \
  --cov=app.schemas.category_schema --cov=app.models.category \
  --cov=app.repositories.category_repository --cov-report=term-missing

# Frontend
npx vitest run src/pages/Categorias/Categorias.test.jsx --coverage
```

| Métrica                                       | Valor                          |
|-----------------------------------------------|--------------------------------|
| `app/models/category.py`                      | 100%                           |
| `app/schemas/category_schema.py`              | 100%                           |
| `app/services/category_service.py`            | 89%                            |
| `app/routes/category_routes.py`               | 87%                            |
| `app/repositories/category_repository.py`     | 0% (código morto - ver DEF-04) |
| **Backend - total (módulos importados)**      | **91%**                        |
| `src/pages/Categorias/Categorias.jsx` (front) | 97,9%                          |

Núcleo da feature acima da meta de **≥ 60%**.

---
## 7. Parecer final

> **Status:** Aprovada com pendências.
>
> Todos os critérios foram exercitados e o comportamento principal está verde
> (**22/25**, cobertura **91%** no backend e **97,9%** na tela). O CRUD funciona, a
> exclusividade por empresa é respeitada e a duplicidade de nome é bloqueada pela
> constraint.
>
> Os defeitos **DEF-01/02/03** e a pendência de refatoração **DEF-04** eram
> **esperados** nesta etapa e **não impedem a aprovação** - estão documentados como
> `xfail` e endereçados pelas issues já abertas (#49, #56, #35). Recomenda-se
> priorizar o **DEF-03** por ser falha de **autorização**.
>
> **Próximos passos (não bloqueantes):**
> 1. **DEF-03** - validar o vínculo `user_company` a partir do `user_id` do JWT *(prioridade)*.
> 2. **DEF-01** - validar duplicidade no service e responder `409` em vez de `500`.
> 3. **DEF-02** - bloquear exclusão de categoria em uso + mensagem na UI.
> 4. **DEF-04** - usar o `category_repository` (hoje código morto) ou removê-lo (refatoração #35).

---
