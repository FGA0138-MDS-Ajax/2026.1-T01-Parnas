## Descrição técnica
Tarefa técnica de qualidade (refatoração). Com as funcionalidades principais implementadas, é necessário padronizar a camada de entrada e saída de dados do backend com DTOs via Marshmallow e revisar o design do frontend para garantir consistência visual entre todas as páginas.

## Rastreabilidade
- **Requisito(s):** — (transversal)
- **Cenário:** Transversal (CEN-00 a CEN-04)
- **Sprint:** 8
- **Prioridade:** Should
- **Tipo:** refactor (backend, frontend)
- **Funcionalidade do produto:** Transversal

## Tarefas Backend — Padronização com DTOs (Marshmallow)
- [ ] Criar schema de entrada (load) e saída (dump) para Usuario
- [ ] Criar schema de entrada (load) e saída (dump) para Empresa
- [ ] Criar schema de entrada (load) e saída (dump) para Categoria
- [ ] Criar schema de entrada (load) e saída (dump) para Transacao
- [ ] Criar schema de entrada (load) e saída (dump) para Conta
- [ ] Criar schema de entrada (load) e saída (dump) para Simulacao
- [ ] Criar schema de entrada (load) e saída (dump) para Documento
- [ ] Aplicar validação via schema em todos os endpoints POST e PUT
- [ ] Garantir que `senha_hash` nunca é retornada em nenhum endpoint
- [ ] Garantir que o `id_empresa` do token JWT é sempre usado no lugar do enviado pelo frontend (evita manipulação)
- [ ] Padronizar formato de resposta de erro: `{ "erro": "mensagem", "campo": "nome_do_campo" }`
- [ ] Padronizar formato de resposta de sucesso: `{ "dados": {}, "mensagem": "mensagem" }`

## Tarefas Frontend — Redesign e Consistência Visual
- [x] Revisar e padronizar a paleta de cores em todas as páginas
- [ ] Criar componentes reutilizáveis em `components/ui/` (Button, Input, Card, Modal, Badge)
- [ ] Substituir elementos HTML puros (button, input) pelos componentes padronizados em todas as páginas
- [ ] Revisar responsividade das páginas Dashboard, Transacoes e Contas
- [x] Padronizar mensagens de sucesso e erro com componente Toast
- [ ] Padronizar layout de listagem (tabela ou cards) entre as páginas
- [x] Revisar Sidebar e Header em `components/layout/`

## Critérios de aceitação
- [ ] Nenhum endpoint retorna dados sem passar pelo schema
- [ ] Nenhuma senha ou dado sensível exposto nas respostas da API
- [ ] Todos os formulários usam os componentes padronizados
- [ ] Visual consistente entre todas as páginas implementadas

## Critérios de teste
- [ ] Testes unitários dos schemas (Pytest)
- [ ] Testes de componentes UI padronizados (Vitest)
- [ ] Cobertura mínima atingida

## Definição de Done
- [ ] Código revisado em pair programming
- [ ] PR aberto de `refactor/dtos-redesign` para `develop`
- [ ] Pull Request revisado pelo par de QA antes do merge na `develop`
- [ ] Documentação técnica atualizada

## Branch
`refactor/dtos-redesign`
