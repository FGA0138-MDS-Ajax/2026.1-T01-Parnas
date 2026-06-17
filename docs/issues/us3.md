## História de usuário
Como Gestor de uma Micro-Empresa, quero recuperar minha senha por email, para não perder acesso à minha conta na plataforma.

## Rastreabilidade
- **Requisito(s):** R05
- **Cenário:** CEN-00 — Plataforma e autenticação
- **Sprint:** 5
- **Prioridade:** Should
- **Funcionalidade do produto:** A — Cadastro e Autenticação de Usuário/Empresa

## Critérios de aceitação
- [ ] Usuário informa email e recebe link de redefinição
- [ ] Link expira em 30 minutos
- [ ] Usuário consegue definir nova senha pelo link
- [ ] Após redefinição, login funciona com nova senha

## Tarefas Backend
- [x] Criar endpoint POST /auth/forgot-password
- [x] Gerar token temporário de redefinição
- [x] Enviar email com link (Flask-Mail)
- [x] Criar endpoint POST /auth/reset-password
- [x] Validar token e atualizar senha no banco

## Tarefas Frontend
- [x] Criar página ForgotPassword/
- [x] Criar formulário com campo email
- [x] Criar página ResetPassword/
- [x] Criar formulário com campos nova senha e confirmação
- [x] Exibir feedback de sucesso/erro em cada etapa

## Critérios de teste
- [ ] Caso(s) de teste do Roteiro cobertos: TS-13
- [ ] Testes unitários escritos (Pytest / Vitest)
- [ ] Testes de integração escritos (se aplicável)
- [ ] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [ ] Cobertura mínima atingida

## Definição de Done
- [ ] Código revisado em pair programming
- [ ] PR aberto de `feature/3-recuperacao-senha` para `develop`
- [ ] Pipeline do GitHub Actions aprovada
- [ ] Branch `test/3-recuperacao-senha` executada pela dupla de QA
- [ ] Documento da feature preenchido
- [ ] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/3-recuperacao-senha`
