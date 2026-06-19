## Descrição técnica
Tarefa de infraestrutura para estabelecer o relacionamento entre as entidades `USUARIO` e `EMPRESA` no ORM, conforme especificado no Diagrama de Classes (Documento de Arquitetura, Seção 2.5.3.1).

O relacionamento definido é: cada `USUARIO` pertence a uma `EMPRESA` via `empresa_id (FK)`. Uma `EMPRESA` pode ter N usuários.

## Rastreabilidade
- **Requisito(s):** R04
- **Cenário:** CEN-00 — Plataforma e autenticação
- **Sprint:** 4
- **Prioridade:** Must
- **Tipo:** infra / banco de dados
- **Funcionalidade do produto:** A — Cadastro e Autenticação de Usuário/Empresa

## Tarefas
- [x] Adicionar `empresa_id (FK)` ao model `usuario.py`
- [x] Configurar relacionamento ORM entre `USUARIO` e `EMPRESA`
- [x] Criar e rodar migration do banco de dados
- [x] Configurar cascata de exclusão nas FKs (deletar empresa remove usuários vinculados)
- [x] Validar que o servidor Flask inicializa sem erros de mapeamento

## Critérios de aceitação
- [x] Relacionamento `USUARIO`–`EMPRESA` mapeado conforme o Diagrama de Classes
- [x] Migration aplicada sem erros em ambiente limpo
- [x] Servidor Flask sobe sem erros de mapeamento ORM

## Critérios de teste
- [x] Caso(s) de teste do Roteiro cobertos: TS-18
- [x] Comportamento de cascata validado via teste de integração

## Definição de Done
- [x] Código revisado em pair programming
- [x] PR aberto de `task/modelagem-usuario-empresa` para `develop`
- [x] Documentação técnica atualizada

## Branch
`task/modelagem-usuario-empresa`
