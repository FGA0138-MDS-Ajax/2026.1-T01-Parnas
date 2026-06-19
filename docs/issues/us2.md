## História de usuário
Como Gestor de uma Micro-Empresa, quero fazer login com email e senha, para acessar minha conta na plataforma.

## Rastreabilidade
- **Requisito(s):** R03
- **Cenário:** CEN-00 — Plataforma e autenticação
- **Sprint:** 4
- **Prioridade:** Must
- **Funcionalidade do produto:** A — Cadastro e Autenticação de Usuário/Empresa

## Critérios de aceitação
- [x] Login com email e senha válidos retorna JWT
- [x] Credenciais inválidas retornam erro com mensagem clara
- [x] Token JWT é armazenado no frontend após login
- [x] Rotas protegidas redirecionam para login se não autenticado

## Tarefas Backend
- [x] Criar endpoint POST /auth/login
- [x] Validar email e senha contra banco
- [x] Gerar e retornar JWT com id_usuario e expiração
- [x] Criar middleware de autenticação para rotas protegidas

## Tarefas Frontend
- [x] Criar página Login/
- [x] Criar formulário com email e senha
- [x] Salvar token JWT no localStorage
- [x] Criar hook useAuth.js
- [x] Proteger rotas autenticadas com React Router
- [x] Redirecionar para dashboard após login bem-sucedido
- [x] Exibir mensagem de erro para credenciais inválidas

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-03, TS-04, TS-12, TS-24
- [x] Testes unitários escritos (Pytest / Vitest)
- [x] Testes de integração escritos (se aplicável)
- [x] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [x] Cobertura mínima atingida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `feature/2-autenticacao-login` para `develop`
- [x] Branch `test/2-autenticacao-login` executada pela dupla de QA
- [x] Documento da feature preenchido
- [x] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/2-autenticacao-login`