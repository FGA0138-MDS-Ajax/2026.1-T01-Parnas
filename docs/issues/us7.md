## História de usuário
Como Gestor de uma Micro-Empresa, quero consultar o histórico completo de movimentações da minha empresa com filtros, para analisar minha situação financeira.

## Rastreabilidade
- **Requisito(s):** R08
- **Cenário:** CEN-01 — Registro de dados financeiros
- **Sprint:** 6
- **Prioridade:** Should
- **Funcionalidade do produto:** D — Histórico de Transações

## Critérios de aceitação
- [x] Gestor visualiza todas as transações da empresa em ordem cronológica
- [x] É possível filtrar por período (data início e data fim)
- [x] É possível filtrar por tipo (receita/despesa)
- [x] É possível filtrar por categoria
- [x] É possível filtrar por valor mínimo e máximo
- [x] Resultado exibe total de receitas, total de despesas e saldo do período filtrado
- [x] Lista é paginada (máximo 20 itens por página)

## Tarefas Banco de Dados
- [x] Criar query de listagem filtrada por período, tipo, categoria e valor
- [x] Criar query de agregação para calcular totais (receitas, despesas, saldo)
- [x] Adicionar índice em data e empresa_id para otimizar buscas
- [x] Implementar paginação na query (LIMIT e OFFSET)

## Tarefas Backend
- [x] Adicionar filtros por período, tipo, categoria e valor no GET /transacoes
- [x] Adicionar parâmetros de paginação (page, per_page)
- [x] Retornar totais (receitas, despesas, saldo) junto com a listagem
- [x] Garantir que apenas transações da empresa autenticada são retornadas

## Tarefas Frontend
- [x] Criar componente de filtros (período, tipo, categoria, valor)
- [x] Exibir totais de receita, despesa e saldo no topo da listagem
- [x] Implementar paginação na listagem
- [x] Atualizar listagem ao aplicar ou limpar filtros
- [x] Criar hook useTransacoes.js para gerenciar estado dos filtros

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-11, TS-17, TS-25
- [x] Testes unitários escritos (Pytest / Vitest)
- [x] Testes de integração escritos (se aplicável)
- [ ] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [x] Cobertura mínima atingida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `feature/7-historico-transacoes` para `develop`
- [x] Branch `test/7-historico-transacoes` executada pela dupla de QA
- [x] Documento da feature preenchido
- [x] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/7-historico-transacoes`

FECHADA
COM PENDÊNCIAS
