## História de usuário
Como Gestor de uma Micro-Empresa, quero cadastrar minha empresa informando seus dados, para vincular minhas movimentações financeiras a ela.

## Rastreabilidade
- **Requisito(s):** R04
- **Cenário:** CEN-00 — Plataforma e autenticação
- **Sprint:** 4
- **Prioridade:** Must
- **Funcionalidade do produto:** A — Cadastro e Autenticação de Usuário/Empresa

## Critérios de aceitação
- [x] Usuário consegue cadastrar empresa com nome e CNPJ obrigatórios
- [x] CNPJ duplicado retorna erro com mensagem clara
- [x] CNPJ é validado (formato e dígitos verificadores)
- [x] Após cadastro, usuário é vinculado automaticamente à empresa

## Tarefas Backend
- [x] Criar model Empresa
- [x] Criar model UsuarioEmpresa
- [x] Criar migrations das tabelas empresa e usuario_empresa
- [x] Criar endpoint POST /empresas
- [x] Validar CNPJ no validators.py
- [x] Vincular automaticamente o usuário criador à empresa

## Tarefas Frontend
- [x] Criar página de cadastro de empresa
- [x] Criar formulário com nome, CNPJ, email e telefone
- [x] Validar CNPJ no frontend (validators.js)
- [x] Integrar com POST /empresas
- [x] Salvar id_empresa no contexto global (EmpresaContext.jsx)

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-18
- [x] Testes unitários escritos (Pytest / Vitest)
- [x] Testes de integração escritos (se aplicável)
- [x] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [x] Cobertura mínima atingida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `feature/4-cadastro-empresa` para `develop`
- [x] Pipeline do GitHub Actions aprovada
- [x] Branch `test/4-cadastro-empresa` executada pela dupla de QA
- [x] Documento da feature preenchido
- [x] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/4-cadastro-empresa`
