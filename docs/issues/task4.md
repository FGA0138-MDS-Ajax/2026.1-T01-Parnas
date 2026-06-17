## Descrição técnica
Tarefa de integração ponta a ponta para consolidar a segurança, o gerenciamento de contas e o ciclo de vida das entidades fundamentais do sistema (`USUARIO` e `EMPRESA`), conforme as regras do Diagrama de Classes e do Documento de Arquitetura.

O escopo engloba:

1. **Autenticação Base:** fluxo de cadastro e login de usuários com geração de tokens JWT.
2. **Contexto de Empresa:** cadastro de empresas protegido por autenticação, vinculando automaticamente o `user_id` do criador e injetando o `empresa_id` no perfil.
3. **Esqueci minha senha:** fluxo de recuperação de conta via envio de e-mail com token temporário de redefinição.
4. **Ciclo de Encerramento:** exclusão segura de usuários e empresas, validando o comportamento de cascata configurado no banco.

## Rastreabilidade
- **Requisito(s):** R01, R03, R04, R05, R02
- **Cenário:** CEN-00 — Plataforma e autenticação
- **Sprint:** 5
- **Prioridade:** Must
- **Tipo:** integração
- **Funcionalidade do produto:** A — Cadastro e Autenticação de Usuário/Empresa

## Tarefas

### 1. Fluxo de Autenticação do Usuário
- [x] Conectar os formulários de **Cadastro de Usuário** e **Login** aos endpoints
- [x] Implementar a captura e o armazenamento seguro do JWT no frontend
- [ ] Configurar o cabeçalho global de requisições (`Authorization: Bearer <token>`) para todas as rotas privadas do React

### 2. Fluxo de Cadastro de Empresa (Protegido)
- [x] Reativar e validar o decorador `@jwt_required()` no endpoint `POST /empresas`
- [x] Ajustar o frontend (`CadastroEmpresa.jsx`) para enviar o CNPJ com a formatação exigida pelo validador do Marshmallow
- [x] Garantir que o backend capture a identidade do usuário logado via `get_jwt_identity()` para salvar o relacionamento correto
- [x] Atualizar o `EmpresaContext` com o `empresa_id` retornado após o cadastro

### 3. Recuperação de Senha
- [x] Integrar a tela de "Esqueci minha senha" com a rota que gera e envia o token de reset
- [x] Criar a tela de "Redefinir Senha" que recebe o token via URL e envia a nova senha
- [x] Tratar cenários de tokens expirados ou inválidos exibindo alertas na interface

### 4. Deleção
- [x] Conectar os botões de exclusão da interface aos endpoints de deleção do backend

## Critérios de aceitação
- [x] O usuário só acessa e submete a tela de Cadastro de Empresa portando um JWT válido
- [x] O fluxo de recuperação gera um e-mail (real/simulado) e permite a alteração segura da senha
- [x] A exclusão de uma empresa limpa as tabelas filhas vinculadas
- [x] Respostas de erro do Flask são interceptadas pelo `catch` do front e exibidas amigavelmente

## Critérios de teste
- [ ] Caso(s) de teste do Roteiro cobertos: TS-12, TS-13, TS-14, TS-18
- [ ] Fluxo homologado de ponta a ponta no ambiente local com a dupla de QA

## Definição de Done
- [ ] Código revisado em pair programming
- [ ] PR aberto integrando as frentes de trabalho para `develop`
- [ ] Funcionalidade homologada de ponta a ponta no ambiente local com a dupla de QA
- [ ] Documentação técnica e rotas atualizadas

## Branch
`task/integracao`
