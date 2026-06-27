## Descrição técnica
Tarefa técnica de qualidade (refatoração). Correção da suíte de testes do backend que
ficou para trás dos refatoramentos (camada de repositórios, mudanças de assinatura nos
services e mudanças de URL nas rotas). O objetivo é deixar a suíte verde novamente,
atualizando os testes ao estado atual do código, sem mascarar defeitos reais.

## Rastreabilidade
- **Requisito(s):** - (transversal)
- **Cenário:** Transversal (CEN-00 a CEN-04)
- **Sprint:** 8
- **Prioridade:** Should
- **Tipo:** refactor (backend - testes)
- **Funcionalidade do produto:** Transversal

## Contexto (defeitos de teste mapeados)
- **feature_4 (cadastro de empresa):** a rota virou `POST /api/companies` (os testes
  batiam em `/api/companies/register`); o service passou a delegar ao `CompanyRepository`
  (os testes unitários mockavam `Company`/`db`/`user_company`); CNPJ duplicado passou a
  levantar `APIException(409)` em vez de retornar tupla.
- **feature_6 (transações):** assinaturas mudaram - `create_transaction(data, user_id)`,
  `update_transaction(transaction_id, user_id, data)`, `delete_transaction(transaction_id, user_id)`;
  o `create` passou a validar `_validate_user_company_access` antes da categoria.
- **feature_8 (exclusão de empresa):** `delete_company(company_id, user_id)` via
  `CompanyRepository`; sem vínculo levanta `APIException(403)`.

## Tarefas
- [x] Atualizar os testes de `feature_4` (unit, integração e e2e) ao estado atual
- [x] Atualizar os testes de `feature_6` (unit e integração) às novas assinaturas
- [x] Atualizar os testes de `feature_8` (unit) ao novo `delete_company`
- [x] Separar defeito real de teste desatualizado e corrigir o que for bug real

## Bug real encontrado (fora do escopo de "teste desatualizado")
- [x] `transaction_routes.py`: as rotas de `update` e `delete` passavam os argumentos na
  ordem errada para o service (dict de dados como `user_id`; `company_id` no lugar do
  `user_id`) e nunca liam `get_jwt_identity()`. A edição quebrava com 500. Corrigido.

## Critérios de teste
- [x] Reexecução da suíte do backend (Pytest) verde: 239 passed, 15 xfailed, 1 xpassed, 0 failed
- [x] Cobertura mantida (os testes foram atualizados, não removidos)
- [x] Suíte do frontend (Vitest) segue verde (90 testes)

## Definição de Done
- [ ] Código revisado em pair programming
- [x] PR aberto de `test/correcao-pos-refactor` para `develop` (PR #83)
- [ ] Pull Request revisado pelo par de QA antes do merge na `develop`
- [ ] Documentação técnica atualizada

## Branch
`test/correcao-pos-refactor`
