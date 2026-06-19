# Documentação de Testes - Recuperação de Senha

## 1. Identificação

| Campo                         | Valor                                  |
|-------------------------------|----------------------------------------|
| **Feature**                   | Recuperação de Senha                   |
| **Cenário**                   | CEN-00                                  |
| **Requisito**                 | R05                                     |
| **Prioridade**                | Should                                  |
| **Branch de desenvolvimento** | `feature/3-recuperacao-senha`          |
| **Branch de teste (QA)**      | `test/feature/3-recuperacao-senha-qa`  |
| **Sprint**                    | 5                                       |
| **Responsáveis (QA)**         | Daniel Filipe / Matheus Moretti        |
| **PR**                        | #71 → `develop`                         |
| **Data**                      | 29/05/2026                             |

> A branch de QA recebeu o sufixo `-qa` para evitar conflito de histórico com a
> branch `test/feature/3-recuperacao-senha` (WIP antiga da dupla de dev, já
> divergente da `develop`).

## 2. Critérios de aceitação testáveis

- [x] Usuário informa e-mail e recebe link de redefinição - `TS-13`, `CT-01`
- [x] Usuário consegue definir nova senha pelo link (token temporário) - `TS-13`, `CT-04`
- [x] Após redefinição, login funciona com a nova senha - `CT-05`
- [ ] **Link expira em 30 minutos** - coberto a nível de mecânica de expiração (`CT-09`), porém o tempo configurado é de **60 min**, não 30 → ver **DEF-01**

## 3. Casos executados

| Caso  | Descrição                                                                | Nível      | Esperado                                       | Observado | Status |
|-------|--------------------------------------------------------------------------|------------|------------------------------------------------|-----------|--------|
| TS-13 | Recuperação de senha via token temporário (gera token → redefine)        | Integração | `200` + "Senha redefinida com sucesso"         | Conforme  | OK      |
| CT-01 | `POST /auth/forgot-password` com e-mail cadastrado                        | Integração | `200` + `reset_link` e `email` no corpo        | Conforme  | OK      |
| CT-02 | `POST /auth/forgot-password` com e-mail não cadastrado                    | Integração | `404` + "Usuário não encontrado"               | Conforme  | OK      |
| CT-03 | `POST /auth/forgot-password` sem o campo e-mail                           | Integração | `400` + "Email obrigatório"                     | Conforme  | OK      |
| CT-04 | `POST /auth/reset-password` com token válido                             | Integração | `200` + "Senha redefinida com sucesso"         | Conforme  | OK      |
| CT-05 | Login passa a funcionar com a senha nova (e a antiga deixa de valer)     | Integração | `401` na senha antiga, `200` + JWT na nova      | Conforme  | OK      |
| CT-06 | `POST /auth/reset-password` com token inválido                           | Integração | `400` + "Token inválido ou expirado"            | Conforme  | OK      |
| CT-07 | `POST /auth/reset-password` sem campos obrigatórios                      | Integração | `400` + "Token e nova senha obrigatórios"       | Conforme  | OK      |
| CT-08 | `generate_reset_token` + `verify_reset_token` (round-trip do e-mail)     | Unitário   | token gera e o e-mail é recuperado idêntico     | Conforme  | OK      |
| CT-09 | `verify_reset_token` com token expirado (`expiration=-1`)               | Unitário   | retorna `None`                                  | Conforme  | OK      |
| CT-10 | `verify_reset_token` com token forjado/inválido                         | Unitário   | retorna `None`                                  | Conforme  | OK      |

> Casos `CT-08`-`CT-10` (token) são autoria do dev Matheus Moretti; os de
> integração (`TS-13`, `CT-01`-`CT-07`) foram adicionados pela QA. Cada arquivo
> de teste traz o marcador `#culpado pelo teste:` indicando o responsável.

## 4. Evidências

### Backend - `python -m pytest tests/unit/feature_3 tests/integration/feature_3 -v`

```
tests/unit/feature_3/test_reset_token.py::test_generate_and_verify_reset_token_success PASSED
tests/unit/feature_3/test_reset_token.py::test_verify_reset_token_expires_correctly PASSED
tests/unit/feature_3/test_reset_token.py::test_verify_reset_token_rejects_invalid_token PASSED
tests/integration/feature_3/test_reset_password_endpoints.py::test_forgot_password_com_email_cadastrado PASSED
tests/integration/feature_3/test_reset_password_endpoints.py::test_forgot_password_com_email_nao_cadastrado PASSED
tests/integration/feature_3/test_reset_password_endpoints.py::test_forgot_password_sem_email PASSED
tests/integration/feature_3/test_reset_password_endpoints.py::test_redefinir_senha_com_token_valido PASSED
tests/integration/feature_3/test_reset_password_endpoints.py::test_login_funciona_apos_redefinicao PASSED
tests/integration/feature_3/test_reset_password_endpoints.py::test_redefinir_senha_com_token_invalido PASSED
tests/integration/feature_3/test_reset_password_endpoints.py::test_redefinir_senha_sem_campos_obrigatorios PASSED
========================= 10 passed, 1 warning in 3.18s =========================
```

### Pipeline (GitHub Actions) - PR #71, run `27782250912`

```
backend   pass   1m10s
frontend  pass   23s
```

Os 10 testes da feature 3 passaram também na execução da CI. (A run total reporta
6 falhas em `tests/.../feature_6` - pré-existentes na `develop`, ver **Nota** abaixo.)

**Total da feature:** 10 testes, 10 passaram, 0 falharam, 0 skip.

## 5. Defeitos encontrados

| ID     | Descrição                                                                                                                                                                                                                                | Status |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| DEF-01 | **Tempo de expiração divergente do critério.** A issue #3 especifica "link expira em **30 minutos**", mas `verify_reset_token` usa `expiration=3600` (**60 min**) por padrão em `app/utils/reset_token.py`. Ajustar para `1800`.        | Aberto |
| DEF-02 | **`/forgot-password` expõe o token na resposta da API** (`reset_link` no corpo do JSON) e o e-mail via Flask-Mail não está efetivamente enviando - o link volta na resposta. Aceitável p/ ambiente de dev, mas inseguro em produção.  | Aberto |
| DEF-03 | **Frontend sem testes automatizados.** As telas `EsqueciSenha/` e `RedefinirSenha/` não possuem testes (Vitest). Cobertura do fluxo de UI está como pendência.                                                                          | Aberto |

> Nota (fora do escopo desta feature): a suíte completa do backend tem 6 testes
> vermelhos em `tests/unit/feature_6` e `tests/integration/feature_6` (assinaturas
> divergentes de `create_transaction`/`update_transaction`/`delete_transaction` -
> `unexpected keyword argument`). São defeitos da **feature 6**, já presentes na
> `develop`, sem relação com a recuperação de senha. Isolados, os 10 testes desta
> feature passam (ver evidências).

## 6. Cobertura

**Backend** - `pytest tests/unit/feature_3 tests/integration/feature_3 --cov=app --cov-report=term-missing` (valores extraídos da run da CI)

| Módulo                        | Cobertura | Observação                                                                       |
|-------------------------------|-----------|---------------------------------------------------------------------------------|
| `app/utils/reset_token.py`    | **100%**  | -                                                                               |
| `app/routes/auth_routes.py`   | **94%**   | não-coberto: `72, 89, 94` - rotas `render_template` das páginas HTML (fora da API) |

Cobertura dos módulos centrais da feature acima da meta de **≥ 60%**.

## 7. Parecer final

**Aprovada com pendências.**

Os critérios de aceitação centrais (solicitar redefinição por e-mail, redefinir a
senha via token temporário e fazer login com a nova senha) estão cobertos por
testes verdes (10/10), com o utilitário de token em **100%** e as rotas de
autenticação em **94%** de cobertura. A pipeline do PR #71 passou (backend e
frontend). O fluxo de redefinição funciona conforme especificado.

**Pendências antes de aprovar sem ressalvas:**
1. **DEF-01** - corrigir o tempo de expiração do token para 30 min (hoje 60 min),
   conforme o critério de aceitação da issue #3.
2. **DEF-02** - remover o token/link da resposta da API e garantir o envio por
   e-mail (Flask-Mail) antes de produção.
3. **DEF-03** - escrever testes de frontend (Vitest) para as telas `EsqueciSenha/`
   e `RedefinirSenha/`.
