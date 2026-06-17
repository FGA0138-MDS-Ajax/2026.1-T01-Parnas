## História de usuário
Como Gestor de uma Micro-Empresa, quero registrar manualmente entradas e saídas financeiras da minha empresa, para manter o histórico financeiro atualizado.

## Rastreabilidade
- **Requisito(s):** R07
- **Cenário:** CEN-01 — Registro de dados financeiros
- **Sprint:** 6
- **Prioridade:** Must
- **Funcionalidade do produto:** C — Cadastro de Transações Financeiras

## Critérios de aceitação
- [ ] Gestor consegue registrar transação com valor, data, tipo e descrição
- [ ] Categoria é obrigatória e listada a partir das categorias da empresa
- [ ] Valor deve ser positivo
- [ ] Data não pode ser futura
- [ ] Transação registrada aparece imediatamente no histórico
- [ ] Gestor consegue editar uma transação existente
- [ ] Gestor consegue excluir uma transação

## Tarefas Banco de Dados
- [x] Criar model Transacao
- [x] Criar migration da tabela transacao
- [x] Criar FKs para empresa, usuario e categoria com cascade configurado
- [x] Criar repository com queries de busca por empresa e filtros básicos

## Tarefas Backend
- [ ] Criar endpoint POST /transacoes
- [ ] Criar endpoint GET /transacoes
- [ ] Criar endpoint PUT /transacoes/<id>
- [ ] Criar endpoint DELETE /transacoes/<id>
- [ ] Validar valor positivo e data não futura
- [ ] Validar que categoria pertence à mesma empresa do usuário autenticado

## Tarefas Frontend
- [x] Criar página Transacoes/
- [x] Criar formulário de nova transação
- [x] Carregar categorias da empresa no select
- [x] Listar transações cadastradas
- [x] Botão de editar transação
- [x] Botão de excluir com confirmação
- [ ] Integrar todos os endpoints
- [x] Exibir feedback de sucesso e erro

## Critérios de teste
- [ ] Caso(s) de teste do Roteiro cobertos: TS-05, TS-16, TS-24
- [ ] Testes unitários escritos (Pytest / Vitest)
- [ ] Testes de integração escritos (se aplicável)
- [ ] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [ ] Cobertura mínima atingida

## Definição de Done
- [ ] Código revisado em pair programming
- [ ] PR aberto de `feature/6-cadastro-transacao` para `develop`
- [ ] Pipeline do GitHub Actions aprovada
- [ ] Branch `test/6-cadastro-transacao` executada pela dupla de QA
- [ ] Documento da feature preenchido
- [ ] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/6-cadastro-transacao`
