## Descrição técnica
**Tarefa VIII - Purificação da Develop.** Consolidar e concluir **todas as pendências antigas** que foram para a develop e que ninguém está corrigindo: integrações de frontend que ficaram em mock/hardcoded/stub, o backend ausente de Contas/Caixas e a higienização da suíte de testes.

Esta issue **não duplica** o que já está rastreado em issues abertas: #35 (Tarefa V - DTOs/redesign), #49 (Fix I - integração de Transações), #54 (Fix II - diferenciação Contas/Transações), #56 (Fix III - integração entre classes), #57 (US16 - Dashboard) e #58 (Tarefa VI - Refactor de Bancos e Rotas).

> **Legenda:** itens marcados com `*` **já foram implementados** em um PR recente que foi **negado** (o **#81** - integração de frontend, negado por conflito com a develop); estão aqui apenas porque ainda não chegaram à develop.

## Rastreabilidade
- **Requisito(s):** - (transversal)
- **Cenário:** Transversal (CEN-00 a CEN-04)
- **Sprint:** 10
- **Prioridade:** Must
- **Tipo:** refactor / qualidade (backend, frontend, banco, testes)
- **Funcionalidade do produto:** Transversal

## Backend
- [x] Criar o backend de **Contas/Caixas (ContaCaixa)**: service + rotas de CRUD vinculadas à empresa (hoje não existe; o front usa `CONTAS_CAIXA_MOCK`)

## Banco de Dados
- [x] Criar o **model** e a **migration** de `ContaCaixa` (tabela de contas bancárias/caixas), com FK para `company`

## Frontend (telas hoje em mock/hardcoded/stub na develop)
- [x] `*` Integrar **Categorias** com a API (CRUD) - hoje hardcoded (`useState([...])`)
- [x] `*` Integrar **ContasCaixa** com a API - hoje `CONTAS_CAIXA_MOCK` (depende do backend de ContaCaixa acima)
- [x] Integrar **Documentos** com a API (upload, listar, download e excluir) - hoje hardcoded
- [x] Integrar **Relatorios** com a API (dados dos gráficos + exportar PDF) - hoje hardcoded
- [x] Integrar a **exclusão de conta e de empresa** (tela `Configuracoes`) com `DELETE /api/profile` e `DELETE /api/companies/<id>` - hoje os handlers só fazem `console.log`

## Testes
- [x] Reconciliar a suíte de **backend**, hoje vermelha após o merge do #76 (os testes assumem contratos antigos: empresa via corpo da requisição em vez da empresa ativa no JWT, retorno por exceção em vez de tupla, etc.)
- [x] Apagar os testes marcados `xfail` e os testes pré-refactor que falham
- [x] Daqui em diante, manter **apenas** testes de **integração** e **e2e**

## Definição de Done
- [x] Suíte de testes da develop **verde** (somente integração + e2e)
- [x] Nenhuma tela de dados usando mock/hardcoded/stub
- [x] `ContaCaixa` com backend + banco + frontend integrados
- [x] PR aberto para a `develop` e revisado pela dupla de QA

## Branch
`task/8-purificacao-develop`
