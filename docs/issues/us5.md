## História de usuário
Como Gestor de uma Micro-Empresa, quero criar categorias personalizadas para minha empresa, para organizar melhor minhas movimentações financeiras.

## Rastreabilidade
- **Requisito(s):** R06
- **Cenário:** CEN-01 — Registro de dados financeiros
- **Sprint:** 5
- **Prioridade:** Must
- **Funcionalidade do produto:** B — Categorização Financeira

## Critérios de aceitação
- [ ] Gestor consegue criar uma categoria com nome e tipo (receita/despesa)
- [ ] Categorias são exclusivas por empresa — outra empresa não as vê
- [ ] Não é possível criar duas categorias com o mesmo nome na mesma empresa
- [ ] Gestor consegue listar todas as categorias da sua empresa
- [ ] Gestor consegue editar o nome de uma categoria existente
- [ ] Gestor consegue excluir uma categoria que não tenha transações vinculadas

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
- [ ] Criar service com validação de categoria duplicada na mesma empresa
- [ ] Criar service com bloqueio de exclusão se houver transações vinculadas
- [ ] Validar que categoria pertence à empresa do usuário autenticado

## Tarefas Frontend
- [x] Criar página Categorias/
- [x] Criar formulário de nova categoria (nome + tipo)
- [x] Listar categorias existentes da empresa
- [x] Botão de editar categoria inline
- [x] Botão de excluir com confirmação
- [ ] Integrar todos os endpoints
- [ ] Exibir mensagem de erro ao tentar excluir categoria em uso

## Critérios de teste
- [ ] Caso(s) de teste do Roteiro cobertos: TS-15
- [ ] Testes unitários escritos (Pytest / Vitest)
- [ ] Testes de integração escritos (se aplicável)
- [ ] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [ ] Cobertura mínima atingida

## Definição de Done
- [ ] Código revisado em pair programming
- [ ] PR aberto de `feature/5-cadastro-categoria` para `develop`
- [ ] Pipeline do GitHub Actions aprovada
- [ ] Branch `test/5-cadastro-categoria` executada pela dupla de QA
- [ ] Documento da feature preenchido
- [ ] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/5-cadastro-categoria`
