# Documentação de Teste - Fix: Exclusão de Conta e Invalidação de Sessão

## 1. Identificação

| Campo                         | Valor                                                                          |
|-------------------------------|--------------------------------------------------------------------------------|
| **Tarefa**                    | Correção da exclusão de conta (soft delete) e bloqueio de sessões/login ativos |
| **Issue relacionada**         | Feature 8 - Exclusão de usuário (complemento de backend)                        |
| **Escopo deste relatório**    | Somente backend (model, migrations, services, auth e rotas)                     |
| **Branch de desenvolvimento** | `fix/exclusao-conta-sessao`                                                      |
| **Branch base comparada**     | `develop`                                                                        |
| **Sprint**                    | 10                                                                               |
| **Responsáveis (QA)**         | Daniel Filipe / Matheus Moretti                                                  |
| **Data**                      | 27/06/2026                                                                       |
| **Evidências**                | Suíte `pytest` (job `backend`) - testes `fix_exclusao_conta`                     |
| **Parecer**                   | **APROVADA** (ver §6)                                                            |

---

## 2. Escopo e fronteira do relatório

O fix resolve, no **backend**, três pontos da exclusão de conta:

- **Soft delete:** excluir a conta deixou de apagar o registro. O usuário passa a
  ter `is_active = False` (novo campo no model `User`, com migration), preservando
  o histórico e os vínculos.
- **Bloqueio de login de conta inativa:** `AuthService.login` rejeita usuário
  inexistente **ou** inativo com `401` e a mensagem `Conta não encontrada ou
  desativada`.
- **Invalidação de sessão ativa:** um `token_in_blocklist_loader` checa, a cada
  requisição autenticada, se o usuário ainda existe e está ativo; um token de
  conta já excluída é bloqueado com `401`.

A avaliação se restringe à área tocada pelo fix. As demais falhas atuais do job
`backend` (features 4, 6 e 8) são **pré-existentes na `develop`** e não foram
introduzidas por esta branch (ver §4).

---

## 3. Casos executados (backend)

Suíte `pytest` nos diretórios `tests/unit/fix_exclusao_conta` e
`tests/integration/fix_exclusao_conta`. **7 testes, 0 falhas.**

| Caso  | Descrição                                                                  | Nível      | Esperado                                              | Status |
|-------|----------------------------------------------------------------------------|------------|-------------------------------------------------------|:------:|
| TS-01 | `delete_user` faz soft delete (marca `is_active=False`, não apaga, commit) | Unitário   | `200`, mensagem de sucesso, sem `delete()` no banco   | Passou |
| TS-02 | `delete_user` em usuário inexistente                                        | Unitário   | `404`, "Usuário não encontrado.", sem commit          | Passou |
| TS-03 | `login` de usuário inativo                                                  | Unitário   | `401`, "Conta não encontrada ou desativada"           | Passou |
| TS-04 | `login` de usuário inexistente                                              | Unitário   | `401`, "Conta não encontrada ou desativada"           | Passou |
| TS-05 | Token de conta excluída é bloqueado ao reutilizar                          | Integração | `DELETE` 1ª vez `200`; reuso do token `401` bloqueado | Passou |
| TS-06 | Login após exclusão da própria conta                                        | Integração | Re-login retorna `401` desativada                     | Passou |
| TS-07 | Preservação dos dados após soft delete                                      | Integração | Registro permanece no banco com `is_active=False`     | Passou |

---

## 4. Evidências

Execução local da suíte do fix (a partir de `backend/`):

```bash
python -m pytest tests/unit/fix_exclusao_conta tests/integration/fix_exclusao_conta -v
```

```
7 passed
```

Suíte completa do backend (`python -m pytest`):

```
38 failed, 208 passed, 15 xfailed, 1 xpassed
```

> **Sobre os 38 *failed*.** São defeitos **pré-existentes na `develop`**, em
> features fora do escopo deste fix, e de natureza de **teste** (não de
> implementação):
> - **Feature 4** (cadastro de empresa): rota `/api/companies/register`
>   retornando `404` e mocks desatualizados (`module ... has no attribute
>   'Company'`/`'find_company'`).
> - **Feature 6** (transações): assinaturas divergentes entre teste e serviço
>   (`unexpected keyword argument 'current_user_id'`/`'company_id'`).
> - **Feature 8** (`test_delete_user_success`): o teste valida o soft delete, mas
>   tem erros de escrita (`assert_not_called(mock_user)` e `is_active()` chamado
>   como função). A implementação do soft delete está correta.
>
> Nenhuma dessas falhas é causada pela branch `fix/exclusao-conta-sessao`. Elas
> seguem como pendência das respectivas issues.

Durante o QA foram corrigidos pequenos defeitos de escrita nos próprios testes do
fix (credenciais que não batiam com a fixture `test_user`, alvo de `patch` com
`app.service` em vez de `app.services`, acento na string esperada e comparação de
`Response` com `int`). Os testes passaram a refletir o comportamento real e
corretamente implementado.

---

## 5. Comportamento verificado

| Cenário                                  | Resultado observado                                  |
|------------------------------------------|------------------------------------------------------|
| Exclusão da própria conta                | `200` - `is_active` vai a `False`, registro mantido  |
| Reuso do token após exclusão             | `401` - "Conta não encontrada ou desativada"         |
| Novo login com conta excluída            | `401` - "Conta não encontrada ou desativada"         |
| Login de conta ativa                     | `200` - token emitido normalmente                    |

---

## 6. Parecer final

**APROVADA.**

O fix é **somente de backend** e está íntegro no seu escopo: implementa o soft
delete (`is_active`), bloqueia o login de contas inativas e invalida tokens de
sessões já excluídas. Os **7 testes** dedicados (`fix_exclusao_conta`, unitários e
de integração) passam, e o comportamento foi conferido caso a caso.

A branch **não introduz regressão**: as 38 falhas atuais do job `backend` são
pré-existentes na `develop`, ligadas a defeitos de teste das features 4, 6 e 8, e
seguem como pendência das próprias issues - fora da fronteira deste fix.
