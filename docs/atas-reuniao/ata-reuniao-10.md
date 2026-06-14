# Ata de Reunião nº 10

---
**Data:** 13/06/2026  
**Horário:** Início: 9h30 — Fim: 11h00  
**Modalidade:** Online (Discord)

---
**Participantes:**
1. Alan Semil dos Santos Vieira
2. Anna Júlia Aparecida Silva Primo
3. Cibelle de Assis Silva
4. Daniel Filipe Borges de Oliveira
5. Eduardo Jesus Dal Pizzol
6. Gabriel Melo Rodrigues Cardone
7. Igor Dantas Araújo
8. João Marcos Santos e Carvalho
9. João Pedro da Nóbrega Souza
10. Júlia Amanda Silva Lima
11. Maria Eduarda de Oliveira Gomes
12. Matheus Moretti Soares

> A presença desta reunião foi registrada e assinada digitalmente via **gov.br** (Lista de Presença nº 3).

---

## Fechamento da Sprint 7, Integração e CI de Testes

- Correções de integração entre as classes e refatoração
- Pipeline de CI de testes (GitHub Actions)
- Abertura das próximas issues

---

## Discussões e Decisões

**Problema identificado no front-end:** Existem **duas páginas semelhantes** no front (Contas a Pagar e Transações). A ambiguidade precisa ser resolvida para que as telas não se sobreponham nem confundam o usuário.

**Infraestrutura e CI de testes:** A estrutura básica de testes (Pytest e Vitest) já foi integrada à `develop` e a refatoração de DTOs do back-end foi mergeada. **Daniel Filipe** se comprometeu a **configurar e corrigir a pipeline de CI de testes no GitHub Actions**, para que as suítes rodem automaticamente a cada Pull Request.

**Compromisso do grupo:** A equipe se comprometeu a **consertar todas as integrações entre as classes** e a **refatorar o que for necessário**, consolidando o que já foi entregue antes de avançar com novas funcionalidades.

**Issues definidas:**

1. **Fluxo de transação com conta:** toda conta paga deve gerar uma transação; resolver a ambiguidade entre a página de Contas a Pagar e a de Transações (não podem ser iguais); a **transação passa a ser uma tabela própria no banco**.
2. **História de usuário — múltiplas empresas:** o usuário pode se cadastrar em várias empresas e precisa **escolher em qual delas vai usar o CrediFab** (empresa ativa).
3. **Dashboard:** integrar ao back-end (o front já está feito).
4. **Integração entre classes:** resolver todos os problemas de integração existentes.

---

## Próximos Passos

1. Daniel Filipe configura a pipeline de CI de testes no GitHub Actions.
2. Implementar o fluxo de transação vinculado às contas e a nova tabela no banco.
3. Resolver a ambiguidade das páginas do front e os problemas de integração entre as classes.
4. Detalhar a seleção de empresa ativa e integrar o dashboard.
Reunião prevista para **20/06/2026**.

---

*Ata elaborada por: Daniel Filipe Borges de Oliveira*
