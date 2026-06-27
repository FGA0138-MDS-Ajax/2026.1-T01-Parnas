## Descrição técnica
**Bug:** as telas de Contas e Transações estão visual e funcionalmente ambíguas, causando confusão sobre o que é um compromisso futuro e o que é uma movimentação já realizada. É necessário corrigir essa sobreposição.

## Rastreabilidade
- **Requisito(s):** R07, R15
- **Cenário:** CEN-01 — Registro de dados financeiros
- **Sprint:** 10
- **Prioridade:** Should
- **Tipo:** fix (frontend, backend, banco de dados)
- **Funcionalidade do produto:** C — Cadastro de Transações / J — Cadastro de Contas

## Tarefas Banco de Dados
- [x] Confirmar que a FK `id_conta` (nullable) existe na tabela `transacao`
- [x] Criar migration caso a FK ainda não exista
- [x] Garantir índice em `id_conta` para consultas de rastreabilidade
- [x] Revisar dados inconsistentes no banco de testes (contas quitadas sem transação correspondente) e corrigir

## Tarefas Backend
- [x] Revisar `PATCH /contas/<id>/quitar` para garantir que sempre cria a transação vinculada (`id_conta` preenchido)
- [x] Garantir que `GET /contas` retorna apenas status "pendente" por padrão (parâmetro opcional para listar quitadas)
- [x] Garantir que `GET /transacoes` não retorna duplicidade quando uma transação tem origem em uma conta

## Tarefas Frontend
- [x] Revisar a página `Contas/` para exibir somente pendentes
- [x] Revisar a página `Transacoes/` para exibir o histórico completo
- [x] Diferenciar visualmente as duas páginas (layout, cores ou ícones)
- [x] Ao quitar conta na tela de Contas, atualizar a lista removendo o item
- [x] Exibir indicador na transação quando ela teve origem em uma conta (badge "Gerado de conta")

## Critérios de conclusão
- [x] Tela de Contas exibe apenas contas com status "pendente"
- [x] Tela de Transações exibe apenas registros já efetivados (histórico)
- [x] Ao marcar uma conta como quitada, ela desaparece da tela de Contas
- [x] Ao quitar uma conta, uma transação correspondente é criada automaticamente e aparece na tela de Transações
- [x] Transação gerada a partir de uma conta mantém referência à conta de origem (`id_conta`)
- [x] As duas telas têm layouts visualmente distintos

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-16, TS-20
- [x] Teste que reproduz o defeito escrito antes do fix
- [x] Cobertura mínima mantida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `fix/diferenciacao-contas-transacoes` para `develop`
- [x] PR revisado pelo par de QA antes do merge na `develop`

## Branch
`fix/diferenciacao-contas-transacoes`
