## História de usuário
Como Gestor de uma Micro-Empresa, quero enviar e organizar documentos fiscais, contábeis e jurídicos da minha empresa em um repositório único, para manter a documentação centralizada e pronta para apresentação a instituições financeiras.

## Rastreabilidade
- **Requisito(s):** R10
- **Cenário:** CEN-02 — Centralização documental para crédito
- **Sprint:** 8
- **Prioridade:** Must
- **Funcionalidade do produto:** G — Centralização Documental

## Critérios de aceitação
- [x] Gestor consegue enviar documento informando nome, tipo e descrição
- [x] Sistema valida tipo e tamanho do arquivo enviado
- [x] Documentos são listados com nome, tipo, data e tamanho
- [x] Gestor consegue baixar um documento enviado
- [x] Gestor consegue excluir um documento com confirmação
- [x] Documentos são exclusivos por empresa — outra empresa não os vê

## Tarefas Banco de Dados
- [x] Criar model Documento com os campos id_documento, id_empresa, id_usuario, nome, tipo, descricao, caminho_arquivo, tamanho, data_upload
- [x] Criar migration da tabela documento
- [x] Criar FK para empresa com CASCADE DELETE
- [x] Criar repository com queries de listagem por empresa e tipo

## Tarefas Backend
- [x] Instalar e configurar gerenciamento de upload de arquivos (multipart/form-data)
- [x] Criar endpoint POST /documentos
- [x] Criar endpoint GET /documentos
- [x] Criar endpoint GET /documentos/<id>/download
- [x] Criar endpoint DELETE /documentos/<id>
- [x] Criar service com validação de tipo e tamanho do arquivo
- [x] Salvar arquivo em pasta local ou serviço de storage (ex: Render Disk)
- [x] Validar que documento pertence à empresa do usuário autenticado

## Tarefas Frontend
- [x] Criar página Documentos/
- [x] Criar componente de upload com drag and drop
- [x] Criar formulário com nome, tipo e descrição do documento
- [x] Listar documentos com nome, tipo, data e tamanho
- [x] Botão de download por documento
- [x] Botão de excluir com confirmação
- [x] Exibir barra de progresso durante upload
- [x] Exibir mensagem de erro para arquivos inválidos ou muito grandes
- [ ] Integrar todos os endpoints (tela Documentos ainda hardcoded na develop, sem chamada à API)

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-19
- [x] Testes unitários escritos (Pytest / Vitest)
- [x] Testes de integração escritos (se aplicável)
- [x] Teste E2E (Playwright) — apenas se a feature pertencer ao fluxo crítico
- [x] Cobertura mínima atingida

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `feature/9-centralizacao-documental` para `develop`
- [x] Pipeline do GitHub Actions aprovada
- [x] Branch `test/9-centralizacao-documental` executada pela dupla de QA
- [x] Documento da feature preenchido
- [x] Status final marcado: aprovada / reprovada / aprovada com pendências

## Branch
`feature/9-centralizacao-documental`
