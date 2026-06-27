## História de usuário
Como Gestor de uma Micro-Empresa, quero poder excluir minha conta de usuário ou encerrar o cadastro da empresa, para remover meus dados da plataforma quando necessário.

## Rastreabilidade
- **Requisito(s):** R02
- **Cenário:** CEN-00 — Plataforma e autenticação
- **Sprint:** 5
- **Prioridade:** Should
- **Funcionalidade do produto:** A — Cadastro e Autenticação de Usuário/Empresa

## Critérios de aceitação
- [x] Gestor consegue excluir a empresa e todos os dados vinculados
- [x] Usuário consegue excluir sua própria conta
- [x] Exclusão de empresa remove categorias e transações vinculadas
- [x] Exclusão de usuário remove seu vínculo com a empresa
- [x] Operação exige confirmação antes de executar
- [x] Usuário não consegue excluir empresa se não for o responsável pela conta

## Tarefas Banco de Dados
- [x] Configurar CASCADE DELETE nas FKs de empresa para categoria, transacao e usuario
- [x] Configurar CASCADE DELETE na FK de usuario para o vínculo com empresa
- [x] Criar migration para adicionar os cascades caso não existam
- [x] Validar no banco que exclusão de empresa remove todos os registros filhos

## Tarefas Backend
- [x] Criar endpoint DELETE /empresas/<id>
- [x] Criar endpoint DELETE /usuarios/<id>
- [x] Validar que apenas o usuário dono da conta pode excluir a empresa
- [x] Impedir que usuário exclua conta de outro usuário

## Tarefas Frontend
- [x] Criar botão de excluir conta nas configurações do usuário
- [x] Criar botão de encerrar empresa nas configurações da empresa
- [x] Criar modal de confirmação com aviso de ação irreversível
- [x] Redirecionar para tela de login após exclusão bem-sucedida
- [x] Integrar com DELETE /empresas e DELETE /usuarios

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-14
- [x] Testes unitários escritos (Pytest / Vitest)
- [x] Testes de integração escritos (comportamento de cascata via API)
- [x] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [x] Cobertura mínima atingida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `feature/8-exclusao-usuario-empresa` para `develop`
- [x] Pipeline do GitHub Actions aprovada
- [x] Branch `test/8-exclusao-usuario-empresa` executada pela dupla de QA
- [x] Documento da feature preenchido
- [x] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/8-exclusao-usuario-empresa`
