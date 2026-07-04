## História de usuário
Como Gestor de uma Micro-Empresa, quero registrar manualmente entradas e saídas financeiras da minha empresa, para manter o histórico financeiro atualizado.

## Rastreabilidade
- **Requisito(s):** R07
- **Cenário:** CEN-01 — Registro de dados financeiros
- **Sprint:** 6
- **Prioridade:** Must
- **Funcionalidade do produto:** C — Cadastro de Transações Financeiras

## Critérios de aceitação
- [x] Gestor consegue registrar transação com valor, data, tipo e descrição
- [x] Categoria é obrigatória e listada a partir das categorias da empresa
- [x] Valor deve ser positivo
- [x] Data não pode ser futura
- [x] Transação registrada aparece imediatamente no histórico
- [x] Gestor consegue editar uma transação existente
- [x] Gestor consegue excluir uma transação

## Tarefas Banco de Dados
- [x] Criar model Transacao
- [x] Criar migration da tabela transacao
- [x] Criar FKs para empresa, usuario e categoria com cascade configurado
- [x] Criar repository com queries de busca por empresa e filtros básicos

## Tarefas Backend
- [x] Criar endpoint POST /transacoes
- [x] Criar endpoint GET /transacoes
- [x] Criar endpoint PUT /transacoes/<id>
- [x] Criar endpoint DELETE /transacoes/<id>
- [x] Validar valor positivo e data não futura
- [x] Validar que categoria pertence à mesma empresa do usuário autenticado

## Tarefas Frontend
- [x] Criar página Transacoes/
- [x] Criar formulário de nova transação
- [x] Carregar categorias da empresa no select
- [x] Listar transações cadastradas
- [x] Botão de editar transação
- [x] Botão de excluir com confirmação
- [x] Integrar todos os endpoints (integração real pendente - ver fix1/fix2; tela ainda em mock/hardcoded na develop)
- [x] Exibir feedback de sucesso e erro

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-05, TS-16, TS-24
- [x] Testes unitários escritos (Pytest / Vitest)
- [x] Testes de integração escritos (se aplicável)
- [x] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [x] Cobertura mínima atingida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `feature/6-cadastro-transacao` para `develop`
- [x] Pipeline do GitHub Actions aprovada
- [x] Branch `test/6-cadastro-transacao` executada pela dupla de QA
- [x] Documento da feature preenchido
- [x] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/6-cadastro-transacao`
