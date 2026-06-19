## História de usuário
Como Gestor de uma Micro-Empresa, quero me cadastrar no sistema informando meus dados, para ter acesso à plataforma.

## Rastreabilidade
- **Requisito(s):** R01
- **Cenário:** CEN-00 — Plataforma e autenticação
- **Sprint:** 4
- **Prioridade:** Must
- **Funcionalidade do produto:** A — Cadastro e Autenticação de Usuário/Empresa

## Critérios de aceitação
- [x] Usuário consegue se cadastrar com nome, email e senha
- [x] Email duplicado retorna erro com mensagem clara
- [x] Senha deve ter no mínimo 8 caracteres
- [x] Cadastro bem-sucedido retorna token JWT

## Tarefas Backend
- [x] Criar model Usuario
- [x] Criar migration da tabela usuario
- [x] Criar endpoint POST /auth/register
- [x] Criar schema de validação (Marshmallow)
- [x] Hash da senha com bcrypt
- [x] Retornar JWT após cadastro

## Tarefas Frontend
- [x] Criar página Register/
- [x] Criar formulário com campos nome, email e senha
- [x] Validação dos campos no frontend
- [x] Integrar com POST /auth/register
- [x] Redirecionar para dashboard após cadastro
- [x] Exibir mensagem de erro em caso de email duplicado

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-01, TS-02, TS-04, TS-24
- [x] Testes unitários escritos (Pytest / Vitest)
- [x] Testes de integração escritos (se aplicável)
- [x] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [x] Cobertura mínima atingida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `feature/1-cadastro-usuario` para `develop`
- [x] Branch `test/1-cadastro-usuario` executada pela dupla de QA
- [x] Documento da feature preenchido
- [x] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/1-cadastro-usuario`