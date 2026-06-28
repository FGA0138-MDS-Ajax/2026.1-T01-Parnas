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
- [x] Criar schema de entrada (load) e saída (dump) para Usuario
- [x] Criar schema de entrada (load) e saída (dump) para Empresa
- [x] Criar schema de entrada (load) e saída (dump) para Categoria
- [x] Criar schema de entrada (load) e saída (dump) para Transacao
- [ ] Criar schema de entrada (load) e saída (dump) para Conta (Bill ainda sem schema Marshmallow na develop)
- [x] Criar schema de entrada (load) e saída (dump) para Simulacao
- [x] Criar schema de entrada (load) e saída (dump) para Documento
- [x] Aplicar validação via schema em todos os endpoints POST e PUT
- [x] Garantir que `senha_hash` nunca é retornada em nenhum endpoint
- [x] Garantir que o `id_empresa` do token JWT é sempre usado no lugar do enviado pelo frontend (evita manipulação)
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
- [x] Nenhuma senha ou dado sensível exposto nas respostas da API
- [ ] Todos os formulários usam os componentes padronizados
- [ ] Visual consistente entre todas as páginas implementadas

## Critérios de teste
- [ ] Testes unitários dos schemas (Pytest)
- [ ] Testes de componentes UI padronizados (Vitest)
- [ ] Cobertura mínima atingida

## Definição de Done
- [ ] Código revisado em pair programming
- [x] PR aberto para `develop` (entregue em dois PRs: `refactor/dtos-backend` e `refactor/redesign-frontend` #59)
- [x] Pull Request revisado pelo par de QA antes do merge na `develop` (QA: Aprovada - ver relatório da Tarefa V)
- [ ] Documentação técnica atualizada

> **Status (auditoria):** os DTOs (Marshmallow) e boa parte do redesign **já estão na develop** (mesclados). Falta, para fechar: schema de Conta (Bill), padronização do formato de resposta (erro/sucesso), componentes reutilizáveis em `components/ui/` e revisão de responsividade. A issue segue **aberta** apenas pelo que falta.

## Branch
`refactor/dtos`
