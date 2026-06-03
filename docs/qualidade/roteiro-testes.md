# Roteiro de Testes (TS-01 a TS-14)

O roteiro de testes define os **casos planejados** para o CrediFab e estabelece a
**rastreabilidade** entre cada caso, o seu nível na pirâmide e o requisito que
ele verifica. A matriz completa é mantida em planilha (Google Sheets, link no
Documento de Visão, seção 6.2); esta página é a versão navegável.

---
## Tabela de casos de teste

| Cód. | Nome | Nível | Requisito |
| :--: | --- | --- | :--: |
| TS-01 | Validação de e-mail e senha no cadastro | Unitário | R01 |
| TS-02 | Geração e validação de token JWT | Unitário | R03 |
| TS-03 | Renderização do formulário de cadastro/login | Unitário | R01, R03 |
| TS-04 | Validação de transação (valor, tipo, categoria) | Unitário | R07 |
| TS-05 | Cadastro de empresa | Unitário | R04 |
| TS-06 | Autenticação e login via JWT | Integração | R03 |
| TS-07 | Recuperação de senha via token temporário | Integração | R05 |
| TS-08 | Exclusão de usuário/empresa com cascata | Integração | R02 |
| TS-09 | Cadastro de categoria por empresa (unicidade) | Integração | R06 |
| TS-10 | Cadastro de transação vinculada à categoria | Integração | R07 |
| TS-11 | Histórico de transações com filtros | Integração | R08 |
| TS-12 | Isolamento de dados entre empresas | Integração | R04 |
| TS-13 | Fluxo E2E: cadastro, login e registro de transação | Sistema | R01, R03, R07 |
| TS-14 | Fluxo E2E: consulta ao histórico financeiro | Sistema | R08 |

---
## Rastreabilidade requisito → Casos

| Requisito | Casos de teste |
| :--: | --- |
| R01 — Cadastro com validação de e-mail/senha | TS-01, TS-03, TS-13 |
| R02 — Exclusão com cascata | TS-08 |
| R03 — Autenticação JWT | TS-02, TS-03, TS-06, TS-13 |
| R04 — Cadastro de empresa / isolamento de dados | TS-05, TS-12 |
| R05 — Recuperação de senha | TS-07 |
| R06 — Categorias por empresa (unicidade) | TS-09 |
| R07 — Transações | TS-04, TS-10, TS-13 |
| R08 — Histórico com filtros | TS-11, TS-14 |

---
## Distribuição por nível

| Nível | Casos | Quantidade |
| --- | --- | :--: |
| Unitário | TS-01, TS-02, TS-03, TS-04, TS-05 | 5 |
| Integração | TS-06, TS-07, TS-08, TS-09, TS-10, TS-11, TS-12 | 7 |
| Sistema (E2E) | TS-13, TS-14 | 2 |

A predominância de casos unitários e de integração reflete a **pirâmide de
testes** adotada pelo grupo (ver [Estratégia](index.md)).

---
## Convenção de status de execução

Ao executar o roteiro em cada Sprint, cada caso recebe um status:

| Status | Significado |
| :--: | --- |
| ✅ Passou | Resultado observado igual ao esperado |
| ❌ Falhou | Divergência → abrir issue `bug` + `fix/<nome>` |
| ⏭️ Não executado | Fora do escopo da Sprint ou bloqueado |
| 🚧 Pendente | Caso depende de feature ainda não entregue |

Os resultados por feature ficam na
[Documentação por Feature](features/index.md) e os agregados nos
[Consolidados por Sprint](sprints/index.md).

---