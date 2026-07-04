## Descrição técnica
Tarefa técnica de qualidade (refatoração). Para suportar o crescimento das próximas USs (Relatórios e Dashboard) com performance e segurança, é necessário padronizar a persistência de dados: remover o acesso direto ao `db.session` de dentro dos Services, movendo essa lógica para **Repositories**, e consolidar os arquivos de migração (`Flask-Migrate`) que ficaram desalinhados após alterações de models.

## Rastreabilidade
- **Requisito(s):** — (transversal)
- **Cenário:** Transversal (CEN-01)
- **Sprint:** 6
- **Prioridade:** Should
- **Tipo:** refactor (backend, banco de dados)
- **Funcionalidade do produto:** Transversal

## Status (reavaliação 27/06/2026)
Feita, com ressalvas. A implementação está na branch **`integration/refactor-banco-rotas`**
(PR **#84** para a `develop`), ainda **não mesclada**. Ressalvas remanescentes: os
services `category` e `comparison` ainda acessam `db.session` diretamente; e a suíte de
testes pós-refactor segue pendente (escopo da task7/task8). Os itens abaixo refletem o
que está pronto na branch.

## Critérios de aceitação
- [x] Camada de `repositories/` criada e estruturada no backend
- [x] Queries complexas de `Transaction`, `Bill` e `Simulation` movidas para seus repositórios
- [x] Services passam a chamar os Repositórios em vez de executar `db.session` diretamente (falta `category` e `comparison`)
- [x] Histórico de migrations limpo e unificado em uma migração inicial estável
- [x] Banco local rodando do zero via `flask db upgrade` sem erros de tabelas ou colunas duplicadas (não revalidado nesta reavaliação)

## Tarefas Banco de Dados (Migrations)
- [x] Apagar a pasta `migrations/` antiga e dropar as tabelas locais no PostgreSQL
- [x] Inicializar o Flask-Migrate do zero: `flask db init`
- [x] Gerar a migração inicial consolidada com todas as tabelas atuais: `flask db migrate -m "initial_schema"`
- [x] Aplicar a migração para validar o ambiente: `flask db upgrade` (não revalidado nesta reavaliação)

## Tarefas Backend (Camada de Repositórios)
- [x] Criar a estrutura de pastas `app/repositories/`
- [x] Implementar o `BaseRepository` (métodos genéricos de CRUD: `save`, `delete`, `find_by_id`)
- [x] Criar repositórios específicos: `UserRepository`, `CompanyRepository`, `TransactionRepository` (isolando a query do índice composto `idx_company_id_date`), `SimulationRepository`
- [x] Refatorar `AuthService` e `TransactionService` para utilizarem os novos repositórios
- [x] Garantir o tratamento correto de sessões do SQLAlchemy entre service e repository (pendente em `category` e `comparison`)

## Critérios de teste
- [x] Reexecução da suíte unitária e de integração após a refatoração (Pytest) (pendente - escopo da task7/fix3)
- [x] Cobertura mínima mantida (pendente - escopo da task7/fix3)

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `integration/refactor-banco-rotas` para `develop` (PR **#84**)
- [x] Documentação técnica atualizada

## Branch
`integration/refactor-banco-rotas`
