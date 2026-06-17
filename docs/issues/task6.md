## Descrição técnica
Tarefa técnica de qualidade (refatoração). Para suportar o crescimento das próximas USs (Relatórios e Dashboard) com performance e segurança, é necessário padronizar a persistência de dados: remover o acesso direto ao `db.session` de dentro dos Services, movendo essa lógica para **Repositories**, e consolidar os arquivos de migração (`Flask-Migrate`) que ficaram desalinhados após alterações de models.

## Rastreabilidade
- **Requisito(s):** — (transversal)
- **Cenário:** Transversal (CEN-01)
- **Sprint:** 6
- **Prioridade:** Should
- **Tipo:** refactor (backend, banco de dados)
- **Funcionalidade do produto:** Transversal

## Critérios de aceitação
- [ ] Camada de `repositories/` criada e estruturada no backend
- [ ] Queries complexas de `Transaction`, `Bill` e `Simulation` movidas para seus repositórios
- [ ] Services passam a chamar os Repositórios em vez de executar `db.session` diretamente
- [ ] Histórico de migrations limpo e unificado em uma migração inicial estável
- [ ] Banco local rodando do zero via `flask db upgrade` sem erros de tabelas ou colunas duplicadas

## Tarefas Banco de Dados (Migrations)
- [ ] Apagar a pasta `migrations/` antiga e dropar as tabelas locais no PostgreSQL
- [ ] Inicializar o Flask-Migrate do zero: `flask db init`
- [ ] Gerar a migração inicial consolidada com todas as tabelas atuais: `flask db migrate -m "initial_schema"`
- [ ] Aplicar a migração para validar o ambiente: `flask db upgrade`

## Tarefas Backend (Camada de Repositórios)
- [ ] Criar a estrutura de pastas `app/repositories/`
- [ ] Implementar o `BaseRepository` (métodos genéricos de CRUD: `save`, `delete`, `find_by_id`)
- [ ] Criar repositórios específicos: `UserRepository`, `CompanyRepository`, `TransactionRepository` (isolando a query do índice composto `idx_company_id_date`), `SimulationRepository`
- [ ] Refatorar `AuthService` e `TransactionService` para utilizarem os novos repositórios
- [ ] Garantir o tratamento correto de sessões do SQLAlchemy entre service e repository

## Critérios de teste
- [ ] Reexecução da suíte unitária e de integração após a refatoração (Pytest)
- [ ] Cobertura mínima mantida

## Definição de Done
- [ ] Código revisado em pair programming
- [ ] PR aberto de `refactor/repositorios-migrations` para `develop`
- [ ] Documentação técnica atualizada

## Branch
`refactor/repositorios-migrations`
