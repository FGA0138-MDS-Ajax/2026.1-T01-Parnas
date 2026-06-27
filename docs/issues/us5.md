## História de usuário
Como Gestor de uma Micro-Empresa, quero criar categorias personalizadas para minha empresa, para organizar melhor minhas movimentações financeiras.

## Rastreabilidade
- **Requisito(s):** R06
- **Cenário:** CEN-01 — Registro de dados financeiros
- **Sprint:** 5
- **Prioridade:** Must
- **Funcionalidade do produto:** B — Categorização Financeira

## Critérios de aceitação
- [x] Gestor consegue criar uma categoria com nome e tipo (receita/despesa)
- [x] Categorias são exclusivas por empresa — outra empresa não as vê
- [x] Não é possível criar duas categorias com o mesmo nome na mesma empresa
- [x] Gestor consegue listar todas as categorias da sua empresa
- [x] Gestor consegue editar o nome de uma categoria existente
- [x] Gestor consegue excluir uma categoria que não tenha transações vinculadas

## Tarefas Banco de Dados
- [x] Criar model Categoria
- [x] Criar migration da tabela categoria
- [x] Criar constraint UNIQUE (id_empresa, nome) para evitar duplicatas
- [x] Criar repository com queries de busca por empresa

## Tarefas Backend
- [x] Criar endpoint POST /categorias
- [x] Criar endpoint GET /categorias
- [x] Criar endpoint PUT /categorias/<id>
- [x] Criar endpoint DELETE /categorias/<id>
- [x] Criar service com validação de categoria duplicada na mesma empresa
- [x] Criar service com bloqueio de exclusão se houver transações vinculadas
- [x] Validar que categoria pertence à empresa do usuário autenticado

## Tarefas Frontend
- [x] Criar página Categorias/
- [x] Criar formulário de nova categoria (nome + tipo)
- [x] Listar categorias existentes da empresa
- [x] Botão de editar categoria inline
- [x] Botão de excluir com confirmação
- [ ] Integrar todos os endpoints (integração real pendente - ver fix1/fix2; tela ainda em mock/hardcoded na develop)
- [x] Exibir mensagem de erro ao tentar excluir categoria em uso

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-15
- [x] Testes unitários escritos (Pytest / Vitest)
- [x] Testes de integração escritos (se aplicável)
- [x] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [x] Cobertura mínima atingida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `feature/5-cadastro-categoria` para `develop`
- [x] Pipeline do GitHub Actions aprovada
- [x] Branch `test/5-cadastro-categoria` executada pela dupla de QA
- [x] Documento da feature preenchido
- [x] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/5-cadastro-categoria`
