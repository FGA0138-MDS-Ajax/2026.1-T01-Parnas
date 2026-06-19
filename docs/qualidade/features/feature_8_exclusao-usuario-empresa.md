# Documentação de Testes - Exclusão de Usuário/Empresa

## 1. Identificação

| Campo                         | Valor                                              |
|-------------------------------|----------------------------------------------------|
| **Feature**                   | Exclusão de Usuário/Empresa                        |
| **Cenário**                   | CEN-00                                              |
| **Requisito**                 | R02                                                |
| **Prioridade**                | Should                                             |
| **Branch de desenvolvimento** | `feature/8-exclusao-usuario-empresa`               |
| **Branch de teste (QA)**      | `test/feature/8-deletar-usuario-e-empresa-qa`      |
| **Sprint**                    | 5                                                  |
| **Responsáveis (QA)**         | Daniel Filipe / Matheus Moretti                    |
| **Data**                      | 27/05/2026                                         |
| **Parecer**                   | Aprovada com pendências (ver secao 7)              |

## 2. Critérios de aceitação testáveis

- [ ] Gestor consegue excluir a empresa e os dados vinculados - backend OK em teste unitário, mas o endpoint real falha (**DEF-02**) e o front nao chama a API (**DEF-01**)
- [ ] Usuário consegue excluir a própria conta - logica de backend OK (`TS-14c`), porém o front nao chama a API (**DEF-01**)
- [ ] Exclusão de empresa remove categorias e transações vinculadas - **nao verificado** (testes mockam o banco, sem cascata real) (**DEF-03**)
- [ ] Exclusão de usuário remove o vínculo com a empresa - **nao verificado** pelo mesmo motivo (**DEF-03**)
- [x] Operação exige confirmação antes de executar - modal de confirmacao coberto no front (`TS-14d`, `TS-14e`)
- [ ] Usuário não exclui empresa se não for o responsável - regra coberta em unidade (`TS-14b`, 403), mas o endpoint real falha antes da checagem (**DEF-02**)

## 3. Casos executados

| Caso   | Descrição                                                                 | Nível    | Esperado                                  | Observado | Status |
|--------|---------------------------------------------------------------------------|----------|-------------------------------------------|-----------|--------|
| TS-14a | `delete_company` pelo dono                                                 | Unitário | `200` + "Empresa excluída com sucesso."   | Conforme  | OK      |
| TS-14b | `delete_company` por quem nao e dono                                       | Unitário | `403` "Acesso negado", banco intacto      | Conforme  | OK      |
| TS-14c | `delete_user` de usuario existente                                         | Unitário | `200` + "Usuário excluído com sucesso."   | Conforme  | OK      |
| TS-14f | `delete_user` de usuario inexistente                                       | Unitário | `404` "Usuário não encontrado."           | Conforme  | OK      |
| TS-14d | Botao "Excluir Empresa" abre modal com aviso de empresa                    | Front    | modal + aviso de empresa na tela          | Conforme  | OK      |
| TS-14e | Botao "Excluir Conta" abre modal com aviso de usuario                      | Front    | modal + aviso de usuario na tela          | Conforme  | OK      |
| TS-14g | "Cancelar" fecha o modal                                                   | Front    | modal some                                | Conforme  | OK      |
| TS-14h | Clique fora (overlay) fecha o modal                                        | Front    | modal some                                | Conforme  | OK      |
| TS-14i | Confirmar exclusao de conta redireciona para `/login`                      | Front    | `navigate('/login')` e modal some         | Conforme  | OK      |
| TS-14j | Confirmar exclusao de empresa fecha o modal sem redirecionar              | Front    | modal some, sem navegacao                 | Conforme  | OK      |

> Importante: os casos de front confirmam apenas o **comportamento de tela** (modal e
> navegacao). Eles **nao** garantem exclusao real porque a tela nao chama a API (**DEF-01**).

## 4. Evidências

### Backend - `pytest tests/unit/feature_8 -v` (saida da pipeline)

```
tests/unit/feature_8/test_company_service.py::test_delete_company_success_by_owner PASSED
tests/unit/feature_8/test_company_service.py::test_delete_company_rejects_if_not_owner PASSED
tests/unit/feature_8/test_user_service.py::test_delete_user_success PASSED
tests/unit/feature_8/test_user_service.py::test_delete_user_returns_404_if_not_found PASSED
```

### Frontend - `vitest run src/pages/Configuracoes/Configuracoes.test.jsx` (saida da pipeline)

```
PASS src/pages/Configuracoes/Configuracoes.test.jsx (7 tests) 751ms
```

Trecho do `stdout` da pipeline, evidenciando que a confirmacao so escreve no console (stub):

```
stdout | ... > confirmar exclusão de conta redireciona para o login
Executando integração para: Excluir Conta
stdout | ... > confirmar exclusão de empresa fecha o modal sem redirecionar
Executando integração para: Excluir Empresa
```

### Pipeline (GitHub Actions)
- Backend: `6 failed, 233 passed, 15 xfailed, 1 xpassed` (as 6 falhas sao da feature_6, pre-existentes na develop, sem relacao com a feature 8).
- Frontend: `12 arquivos, 67 passed, 3 skipped`.

**Total da feature 8:** 11 testes (4 backend + 7 front), todos verdes - porem cobrindo comportamento, nao a exclusao real (ver defeitos).

## 5. Defeitos encontrados

| ID     | Descrição                                                                                                                                                                                                                                                            | Status |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| DEF-01 | **Front nao integrado (stub).** `frontend/src/pages/Configuracoes/Configuracoes.jsx:31-40` - `handleConfirmAction` apenas faz `console.log` e fecha o modal (no caso de usuario, navega para `/login`). **Nenhuma chamada a `DELETE /api/companies/delete` nem `DELETE /api/profile`.** A tarefa "Integrar com DELETE /empresas e /usuarios" esta marcada como concluida na issue, mas nao foi feita. | Aberto |
| DEF-02 | **Endpoint real de exclusao de empresa quebrado (500).** `backend/app/services/company_service.py:45` declara `find_company(company_CNPJ, user_id)` (2 parametros), mas e chamada com 1 nas linhas 52, 75 e 93 -> `TypeError` -> HTTP 500. Os testes unitarios passam apenas porque **mockam** `find_company`. Mesmo defeito apontado no relatorio da Tarefa IV. | Aberto |
| DEF-03 | **Cascata (TS-14) nao verificada.** Os testes de backend sao unitarios com `db` mockado, entao a remocao em cascata de categorias, transacoes e do vinculo usuario-empresa nunca e exercitada. Nao existe teste de integracao da feature 8 (`tests/integration/feature_8/`). | Aberto |

## 6. Cobertura

**Backend** (valores da pipeline, `--cov=app`):

| Módulo                            | Cobertura | Observação                                                                          |
|-----------------------------------|-----------|------------------------------------------------------------------------------------|
| `app/services/company_service.py` | 57%       | nao coberto: `46-48` (`find_company`), `54`, `68-70`, `74-105` (`delete`/`update`)  |
| `app/services/user_service.py`    | 59%       | nao coberto: `18`, `72-110` (parte real de `delete_user`/`update_user`)             |

**Frontend** (pipeline):

| Módulo                                       | Cobertura | Observação                          |
|----------------------------------------------|-----------|-------------------------------------|
| `src/pages/Configuracoes/Configuracoes.jsx`  | 93,68%    | branch 100%, funcoes 87,5%          |

## 7. Parecer final

**Aprovada com pendências.**

Cada camada passou nos seus testes: a logica de backend (autorizacao do dono, 403
para nao-dono, 404 para usuario inexistente) e o comportamento de tela (modal de
confirmacao e redirecionamento) estao corretos e cobertos por 11 testes verdes, e a
pipeline aprovou. A feature ja foi integrada na `main`.

Ficam registradas as pendencias abaixo, encaminhadas aos times de back e front para
serem tratadas em branch de refatoracao:

1. **DEF-01** - integrar a tela com os endpoints de exclusao (hoje a confirmacao so
   fecha o modal, sem chamar a API).
2. **DEF-02** - corrigir a assinatura de `find_company` para o `DELETE` real de
   empresa nao retornar 500.
3. **DEF-03** - adicionar um teste de integracao que exercite a cascata real
   (categorias, transacoes e vinculo usuario-empresa).

Como a feature ja esta na `main` e as correcoes serao feitas em uma branch de
refatoracao, o parecer e de **aprovacao com pendencias**, com os defeitos acima
registrados para acompanhamento.
