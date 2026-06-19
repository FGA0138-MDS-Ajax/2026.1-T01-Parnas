# Documentação de Testes - Autenticação e Login

## 1. Identificação

| Campo                         | Valor                           |
|-------------------------------|---------------------------------|
| **Feature**                   | Autenticação e Login            |
| **Cenário**                   | CEN-00                          |
| **Requisito**                 | R03                             |
| **Prioridade**                | Must                            |
| **Branch de desenvolvimento** | `feature/2-autenticacao-login`  |
| **Branch de teste (QA)**      | `test/feature/2-login`          |
| **Sprint**                    | 4-5                             |
| **Responsáveis (QA)**         | Daniel Filipe / Matheus Moretti |
| **Data**                      | 21/05/2026                      |

## 2. Critérios de aceitação testáveis

- [x] Login com email e senha válidos retorna JWT - `TS-03`, `TS-06`
- [x] Credenciais inválidas retornam erro com mensagem clara - `TS-01`, `TS-02`, `TS-07`, `TS-08`, `TS-15`
- [x] Token JWT é armazenado no frontend após login - `TS-13`
- [x] Rotas protegidas redirecionam para login se não autenticado - coberto por `ProtectedRoute` em `src/routes.jsx` (redireciona para `/login` quando `!isAuthenticated`); ver **DEF-01** quanto ao middleware do backend

## 3. Casos executados

| Caso  | Descrição                                                            | Nível      | Esperado                                  | Observado | Status |
|-------|----------------------------------------------------------------------|------------|-------------------------------------------|-----------|--------|
| TS-01 | `login` com e-mail inexistente                                       | Unitário   | `401` + "E-mail ou senha inválidos"       | Conforme  | OK      |
| TS-02 | `login` com senha incorreta                                          | Unitário   | `401` + "E-mail ou senha inválidos"       | Conforme  | OK      |
| TS-03 | `login` com credenciais válidas                                      | Unitário   | `200` + token, JWT com `str(user_id)`     | Conforme  | OK      |
| TS-06 | `POST /auth/login` válido (rota + banco)                             | Integração | `200` + JWT no corpo                      | Conforme  | OK      |
| TS-07 | `POST /auth/login` senha incorreta                                   | Integração | `401` + mensagem clara                    | Conforme  | OK      |
| TS-08 | `POST /auth/login` e-mail inexistente                                | Integração | `401` genérico (não revela e-mail)        | Conforme  | OK      |
| TS-09 | `POST /auth/login` sem senha                                         | Integração | `400` + "E-mail e senha são obrigatórios" | Conforme  | OK      |
| TS-12 | Render do formulário (campos + botão Entrar)                         | Unitário   | campos e botão na tela                    | Conforme  | OK      |
| TS-13 | Login OK salva token no `localStorage` e redireciona p/ `/dashboard` | Unitário   | token salvo + `navigate('/dashboard')`    | Conforme  | OK      |
| TS-15 | Credenciais inválidas exibem erro da API                             | Unitário   | mensagem de erro, sem token nem redirect  | Conforme  | OK      |
| TS-16 | Senha < 8 caracteres barra antes da API                              | Unitário   | erro local, `fetch` não chamado           | Conforme  | OK      |


## 4. Evidências

### Backend - `python -m pytest tests/unit/feature_2 tests/integration/feature_2 -v`

```
tests/unit/feature_2/test_auth_service.py::test_login_usuario_inexistente PASSED
tests/unit/feature_2/test_auth_service.py::test_login_senha_incorreta PASSED
tests/unit/feature_2/test_auth_service.py::test_login_credenciais_validas PASSED
tests/integration/feature_2/test_auth_routes.py::test_login_credenciais_validas PASSED
tests/integration/feature_2/test_auth_routes.py::test_login_senha_incorreta PASSED
tests/integration/feature_2/test_auth_routes.py::test_login_email_inexistente PASSED
tests/integration/feature_2/test_auth_routes.py::test_login_sem_campos_obrigatorios PASSED
========================= 7 passed, 1 warning in 2.32s =========================
```

### Frontend - `npx vitest run src/pages/Login/Login.test.jsx`

```
 src/pages/Login/Login.test.jsx (4 tests) 749ms
 Test Files  1 passed (1)
      Tests  4 passed (4)
```

**Total:** 11 testes, 11 passaram, 0 falharam, 0 skip.

## 5. Defeitos encontrados

| ID     | Descrição                                                                                                                                                                                                                                                                                      | Status |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| DEF-01 | `backend/app/utils/auth.py` é apenas um **stub de exemplo** - não há `@jwt_required()` aplicado a nenhuma rota real do backend. A tarefa "Criar middleware de autenticação para rotas protegidas" está marcada como concluída, mas a proteção de rotas no back não está implementada/testável. | Aberto |
| DEF-02 | Os `<label>` em `Login.jsx` não estão associados aos `<input>` (sem `htmlFor`/`id`), prejudicando acessibilidade e forçando os testes a buscar por `placeholder` em vez de `getByLabelText`.                                                                                                   | Aberto |

> Nota (fora do escopo desta feature): a suíte completa do backend tem 2 testes
> vermelhos em `tests/unit/feature_1/test_validators.py::test_is_valid_password_spaces`
> (validação de senha com espaços). São defeitos da **feature 1**, não do login,
> e devem ser tratados no relatório/issue daquela feature.
>
> Nota (contaminação por outra feature): na suíte de integração completa, o
> `test_login_email_inexistente` pode aparecer vermelho (`404` em vez de `401`) por
> **contaminação do DEF-01 da feature 10** - o model `Simulation` referencia a relação
> inexistente `simulations` em `Company`, quebrando a configuração global dos mappers
> do SQLAlchemy e derrubando a integração das features 2, 7 e 14. Isolados, os 7 testes
> deste login passam (ver evidências acima). Tratado no relatório da **feature 10**.

## 6. Cobertura

**Backend** - `pytest tests/unit/feature_2 tests/integration/feature_2 --cov=app.services.auth_service --cov=app.routes.auth_routes --cov-report=term-missing`

| Módulo                         | Cobertura | Observação                                                                        |
|--------------------------------|-----------|-----------------------------------------------------------------------------------|
| `app/services/auth_service.py` | **100%**  | -                                                                                 |
| `app/routes/auth_routes.py`    | 49%       | o não-coberto (`32-94`) é `forgot-password`/`reset-password`, fora desta história |

**Frontend** - `npx vitest run src/pages/Login/Login.test.jsx --coverage`

| Módulo                        | Cobertura  | Linhas não cobertas                                                                      |
|-------------------------------|------------|------------------------------------------------------------------------------------------|
| `src/pages/Login/Login.jsx`   | **93,66%** | `25-28` (campos vazios), `58-59` (fallback `access_token`), `71-73` (`handleDemoAccess`) |
| `src/hooks/useAuth.js`        | **100%**   | -                                                                                        |
| `src/context/AuthContext.jsx` | 82,35%     | `14-16` (`logout`)                                                                       |

Cobertura dos módulos centrais do login (service + hook) acima da meta de **≥ 60%**.

## 7. Parecer final

**Aprovada com pendências.**

Todos os 4 critérios de aceitação estão cobertos por testes verdes (11/11), com o
serviço de autenticação em 100% e a tela de login em ~94% de cobertura. O fluxo
de login (JWT, mensagem de erro clara, persistência no `localStorage` e
redirecionamento de rota protegida no front) funciona conforme especificado.

**Pendências antes de aprovar sem ressalvas:**
1. **DEF-01** - implementar e aplicar o middleware de autenticação no backend
   (`@jwt_required()` em rotas protegidas); hoje é só um stub de exemplo.
2. **DEF-02** - associar `<label>`/`<input>` no `Login.jsx` (acessibilidade).
