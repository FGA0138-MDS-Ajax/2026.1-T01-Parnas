# Backlog de Issues

Esta seção reúne as **issues** do CrediFab (histórias de usuário, tarefas técnicas e
correções), padronizadas e rastreáveis ao [Backlog do Produto](../produto/visao.md),
ao [Roteiro de Testes](../qualidade/roteiro-testes.md) e aos
[Cenários funcionais](../produto/visao.md).

Cada issue traz: **História/Descrição**, **Rastreabilidade** (requisito, cenário,
Sprint, prioridade, funcionalidade), **critérios de aceitação**, **tarefas**,
**critérios de teste** (casos TS do roteiro) e a **Definição de Done**.

> A numeração `#` das issues no GitHub é irrelevante para esta documentação — a
> rastreabilidade é feita por **requisito (R0X)**, **cenário (CEN-0X)** e **caso de
> teste (TS-0X)**.

---
## Histórias de Usuário

| Issue | Título | Func. | Req. | Cenário | Sprint | Status |
|-------|--------|:----:|:----:|:------:|:------:|--------|
| [us1](us1.md) | Cadastro de usuário | A | R01 | CEN-00 | 4 | ✅ Fechada |
| [us2](us2.md) | Autenticação e login | A | R03 | CEN-00 | 4 | ✅ Fechada |
| [us4](us4.md) | Cadastro de empresa | A | R04 | CEN-00 | 4 | 🔄 Aberta |
| [us3](us3.md) | Recuperação de senha | A | R05 | CEN-00 | 5 | 🔄 Aberta |
| [us8](us8.md) | Exclusão de usuário/empresa | A | R02 | CEN-00 | 5 | 🔄 Aberta |
| [us5](us5.md) | Cadastro de categoria | B | R06 | CEN-01 | 5 | 🔄 Aberta |
| [us6](us6.md) | Cadastro de transação | C | R07 | CEN-01 | 6 | 🔄 Aberta |
| [us7](us7.md) | Histórico de transações | D | R08 | CEN-01 | 6 | 🚧 Fechada com pendências |
| [us16](us16.md) | Dashboard financeiro | E | R09 | CEN-01 | 7 | 🔄 Aberta |
| [us11](us11.md) | Cadastro de contas | J | R15 | CEN-01 | 7 | 🔄 Aberta |
| [us15](us15.md) | Seleção de empresa ativa | A | R04 | CEN-00 | 7 | 🔄 Aberta |
| [us9](us9.md) | Centralização documental | G | R10 | CEN-02 | 8 | 🔄 Aberta |
| [us12](us12.md) | Relatórios financeiros | F | R11 | CEN-03 | 8 | 🔄 Aberta |
| [us10](us10.md) | Simulação de crédito *(frontend)* | H | R12 | CEN-04 | 9 | 🚧 Fechada com pendências |
| [us13](us13.md) | Simulação de crédito *(backend)* | H | R12 | CEN-04 | 9 | 🔄 Aberta |
| [us14](us14.md) | Comparação de modalidades de crédito | I | R13 | CEN-04 | 9 | 🚧 Fechada com pendências |

---
## Tarefas Técnicas

| Issue | Título | Tipo | Sprint | Status |
|-------|--------|------|:------:|--------|
| [task2](task2.md) | Configuração do GitHub Pages / MkDocs | infra | 3 | ✅ Fechada |
| [task3](task3.md) | Estrutura base de testes | infra | 3 | ✅ Fechada |
| [task1](task1.md) | Modelagem Usuário–Empresa (ORM) | infra | 4 | ✅ Fechada |
| [task4](task4.md) | Integração de autenticação e ciclo de vida | integração | 5 | 🔄 Aberta |
| [task6](task6.md) | Repositórios e consolidação de migrations | refactor | 6 | 🔄 Aberta |
| [task5](task5.md) | DTOs (Marshmallow) e redesign do frontend | refactor | 8 | 🔄 Em andamento |

---
## Correções (fix)

| Issue | Título | Tipo | Sprint | Status |
|-------|--------|------|:------:|--------|
| [fix1](fix1.md) | Integração da aba de Transações com a API | fix | 10 | 🔄 Em andamento |
| [fix4](fix4.md) | Exclusão de conta não invalida a sessão | fix | 10 | 🔄 Em andamento |
| [fix2](fix2.md) | Diferenciação entre Contas e Transações | fix | 10 | 🔄 Em andamento |
| [fix3](fix3.md) | Consolidação das integrações entre classes | refactor | 10 | 🔄 Em andamento |

> A Sprint 10 concentra a **estabilização e refatoração**: consolidação dos defeitos
> mapeados nas Sprints anteriores e revisão das integrações antes da entrega final.
