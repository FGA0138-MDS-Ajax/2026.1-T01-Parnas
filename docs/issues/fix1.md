## Descrição técnica
**Bug:** a aba de Transações ainda exibe dados *mock* no frontend em vez de consumir os endpoints reais da API. Toda a camada de dados precisa ser substituída pela integração real com o backend.

## Rastreabilidade
- **Requisito(s):** R07, R08
- **Cenário:** CEN-01 - Registro de dados financeiros
- **Sprint:** 10
- **Prioridade:** Must
- **Tipo:** fix (frontend, backend)
- **Funcionalidade do produto:** C - Cadastro de Transações Financeiras

## Tarefas Frontend
- [ ] Remover todos os dados mock do arquivo de `Transacoes/`
- [ ] Integrar listagem com `GET /transacoes`
- [ ] Integrar criação com `POST /transacoes`
- [ ] Integrar edição com `PUT /transacoes/<id>`
- [ ] Integrar exclusão com `DELETE /transacoes/<id>`
- [ ] Integrar filtros (período, tipo, categoria) com os query params da API
- [ ] Integrar totais (receitas, despesas, saldo) retornados pela API
- [ ] Integrar paginação com os parâmetros `page` e `per_page`
- [x] Garantir que o `id_empresa` vem do contexto autenticado (`EmpresaContext`)
- [x] Exibir loading enquanto aguarda resposta da API
- [x] Exibir mensagem de erro em caso de falha na requisição

## Tarefas Backend
- [ ] Verificar se `GET /transacoes` retorna os filtros corretamente
- [ ] Verificar se os totais (receitas, despesas, saldo) são calculados e retornados junto com a listagem
- [ ] Verificar se a paginação está funcionando

## Critérios de conclusão
- [ ] Nenhum dado mock presente na aba de Transações
- [ ] Todas as operações CRUD funcionando com dados reais
- [ ] Filtros e totais refletindo dados do banco

## Critérios de teste
- [ ] Caso(s) de teste do Roteiro cobertos: TS-16, TS-17
- [ ] Teste que reproduz o defeito escrito antes do fix
- [x] Cobertura mínima mantida

## Definição de Done
- [ ] Código revisado em pair programming
- [ ] PR aberto de `fix/integracao-transacoes` para `develop`
- [ ] PR revisado pelo par de QA antes do merge na `develop`

## Branch
`fix/integracao-transacoes`
