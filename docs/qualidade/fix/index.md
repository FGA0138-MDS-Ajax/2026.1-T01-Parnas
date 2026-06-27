# Documentação de Testes por Correção (fix)

Quando um defeito é mapeado, a dupla de Qualidade abre uma issue de `fix` e, após
a correção, produz um **relatório de QA próprio** para a branch de correção - com
identificação, casos executados, evidências e o **parecer** sobre a integridade do
fix.

Diferente das **features** (validadas durante o desenvolvimento) e das **tarefas
técnicas** (avaliadas com rigor de "Aprovada" ou "Reprovada"), as correções podem
ainda carregar **pendências** de outras frentes - registradas explicitamente no
relatório.

---
## Relatórios disponíveis

| Correção | Escopo | Sprint | Status |
|---|---|:--:|---|
| [Contas e Transações (fix1 e fix2)](fix_1_e_2_contas-transacoes.md) | Frontend - Contas / Transações / ContasCaixa | 10 | Aprovada |
| [Exclusão de Conta e Sessão (fix4)](fix_exclusao-conta-sessao.md) | Backend - Exclusão de usuário / Autenticação | 10 | Aprovada |
| [Integração real de Transações e Contas](fix_integracao-transacoes.md) | Backend Contas / Frontend Transações e Contas | 10 | Aprovada com pendências |

---
## Status possíveis

| Status                         | Significado                                               |
|--------------------------------|-----------------------------------------------------------|
| **Aprovada**                 | Correção íntegra no seu escopo; pode ser mesclada         |
| **Aprovada com pendências** | Corrige o alvo, mas há itens de outras frentes em aberto  |
| **Reprovada**                | A correção não resolve o defeito; volta para desenvolvimento |
