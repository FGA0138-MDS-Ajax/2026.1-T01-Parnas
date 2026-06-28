## Descrição técnica
**Bug:** ao excluir uma conta de usuário, ainda é possível realizar login com as credenciais da conta excluída. O backend não está invalidando corretamente o acesso após a exclusão.

## Rastreabilidade
- **Requisito(s):** R02, R03
- **Cenário:** CEN-00 - Plataforma e autenticação
- **Sprint:** 10
- **Prioridade:** Must
- **Tipo:** fix (backend)
- **Funcionalidade do produto:** A - Cadastro e Autenticação de Usuário/Empresa

## Tarefas Backend
- [x] Criar controle de tokens invalidados:
      - Opção A - adicionar campo `ativo` (boolean) em `USUARIO` e checar a cada requisição autenticada
      - Opção B - criar tabela `TOKEN_BLOCKLIST` com os tokens revogados
- [x] Criar migration para a solução escolhida
- [x] Atualizar o middleware de autenticação para verificar se o usuário ainda está ativo antes de processar a requisição
- [x] Garantir que ao deletar usuário o campo `ativo` vira `False` (ou o token é adicionado à blocklist)
- [x] Garantir que login com conta excluída retorna 401 com a mensagem "Conta não encontrada ou desativada"
- [x] Garantir que requisições com token de usuário excluído retornam 401

## Tarefas Frontend
- [ ] Tratar resposta 401 de "conta desativada" no interceptor do Axios
- [ ] Redirecionar para a tela de login ao receber esse 401
- [ ] Limpar token do `localStorage` ao detectar conta desativada

## Critérios de conclusão
- [x] Login com conta excluída retorna erro 401
- [x] Token de usuário excluído é rejeitado em todas as rotas protegidas
- [ ] Frontend redireciona corretamente ao detectar conta inativa

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-14
- [x] Teste que reproduz o defeito escrito antes do fix
- [x] Cobertura mínima mantida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `fix/exclusao-conta-sessao` para `develop`
- [x] PR revisado pelo par de QA antes do merge na `develop`

## Branch
`fix/exclusao-conta-sessao`
