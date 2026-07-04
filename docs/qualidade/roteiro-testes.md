# Roteiro de Testes 

O roteiro de testes define os **casos planejados** para o CrediFab e estabelece a
**rastreabilidade** entre cada caso, o seu nível na pirâmide, o tipo de teste e o
requisito que ele verifica. A matriz completa (pré-condições, passos, dados de
entrada, resultado esperado e status) é mantida em planilha (Google Sheets, link
no Documento de Visão, seção 6.2); esta página é a versão navegável.

> Esta versão acompanha o **Documento de Visão v2.3** (Tabela 12).

---
## Tabela de casos de teste

| Cód.  | Nome                                                               | Nível      | Tipo          |   Requisito   |
|:-----:|--------------------------------------------------------------------|------------|---------------|:-------------:|
| TS-01 | Validação de e-mail e senha no cadastro de usuário                 | Unitário   | Funcional     |      R01      |
| TS-02 | Validação de data de nascimento e idade mínima                     | Unitário   | Funcional     |      R01      |
| TS-03 | Geração e validação de token JWT                                   | Unitário   | Funcional     |      R03      |
| TS-04 | Renderização dos formulários de cadastro e login                   | Unitário   | Funcional     |   R01, R03    |
| TS-05 | Validação de transação (valor, tipo, categoria)                    | Unitário   | Funcional     |      R07      |
| TS-06 | Cálculo de financiamento pela Tabela Price                         | Unitário   | Funcional     |      R12      |
| TS-07 | Cálculo de financiamento pelo SAC                                  | Unitário   | Funcional     |      R12      |
| TS-08 | Projeção de impacto no fluxo de caixa                              | Unitário   | Funcional     |      R12      |
| TS-09 | Cálculo e destaque da modalidade mais vantajosa                    | Unitário   | Funcional     |      R13      |
| TS-10 | Alerta de modalidade de pessoa física                              | Unitário   | Funcional     |      R13      |
| TS-11 | Filtros e paginação do histórico (hook de UI)                      | Unitário   | Funcional     |      R08      |
| TS-12 | Autenticação e login via token JWT                                 | Integração | Funcional     |      R03      |
| TS-13 | Recuperação de senha via token temporário                          | Integração | Funcional     |      R05      |
| TS-14 | Exclusão de usuário/empresa com cascata nas FKs                    | Integração | Funcional     |      R02      |
| TS-15 | Cadastro de categoria por empresa (unicidade)                      | Integração | Funcional     |      R06      |
| TS-16 | Cadastro de transação vinculada à categoria via API                | Integração | Funcional     |      R07      |
| TS-17 | Histórico de transações com filtros e totais                       | Integração | Funcional     |      R08      |
| TS-18 | Isolamento de dados entre empresas (vínculo usuário-empresa)       | Integração | Funcional     |      R04      |
| TS-19 | Upload e organização de documentos                                 | Integração | Funcional     |      R10      |
| TS-20 | Cadastro de contas a pagar/receber                                 | Integração | Funcional     |      R15      |
| TS-21 | Geração de relatório financeiro em PDF                             | Integração | Funcional     |      R11      |
| TS-22 | Endpoints de simulação de crédito (calcular/salvar/listar/excluir) | Integração | Funcional     |      R12      |
| TS-23 | Endpoints de comparação de modalidades                             | Integração | Funcional     |      R13      |
| TS-24 | Fluxo E2E de cadastro, login e registro de transação               | Sistema    | Funcional     | R01, R03, R07 |
| TS-25 | Fluxo E2E de consulta ao histórico financeiro com filtros          | Sistema    | Funcional     |      R08      |
| TS-26 | Fluxo E2E de contas a pagar e quitação gerando transação           | Sistema    | Funcional     |   R15, R07    |
| TS-27 | Teste de carga no endpoint de simulação de crédito (Locust)        | Carga      | Não funcional |      R14      |

---
## Rastreabilidade requisito → casos

|                       Requisito                       | Casos de teste                    |
|:-----------------------------------------------------:|-----------------------------------|
|     R01 - Cadastro com validação de e-mail/senha      | TS-01, TS-02, TS-04, TS-24        |
|              R02 - Exclusão com cascata               | TS-14                             |
|                R03 - Autenticação JWT                 | TS-03, TS-04, TS-12, TS-24        |
| R04 - Modelagem Usuário-Empresa / isolamento de dados | TS-18                             |
|              R05 - Recuperação de senha               | TS-13                             |
|       R06 - Categorias por empresa (unicidade)        | TS-15                             |
|                   R07 - Transações                    | TS-05, TS-16, TS-24, TS-26        |
|              R08 - Histórico com filtros              | TS-11, TS-17, TS-25               |
|              R09 - Dashboard financeiro               | TS-17                             |
|            R10 - Centralização documental             | TS-19                             |
|          R11 - Relatórios financeiros (PDF)           | TS-21                             |
|        R12 - Simulação de crédito (Price/SAC)         | TS-06, TS-07, TS-08, TS-22        |
|            R13 - Comparação de modalidades            | TS-09, TS-10, TS-23               |
|                   R14 - Desempenho                    | TS-27                             |
|               R15 - Cadastro de contas                | TS-20, TS-26                      |

---
## Distribuição por nível

| Nível         | Casos               | Quantidade |
|---------------|---------------------|:----------:|
| Unitário      | TS-01 … TS-11       |     11     |
| Integração    | TS-12 … TS-23       |     12     |
| Sistema (E2E) | TS-24, TS-25, TS-26 |     3      |
| Carga         | TS-27               |     1      |

A predominância de casos unitários e de integração reflete a **pirâmide de
testes** adotada pelo grupo (ver [Estratégia](index.md)).

---
## Convenção de status de execução
Ao executar o roteiro em cada Sprint, cada caso recebe um status:

|    Status     | Significado                                    |
|:-------------:|------------------------------------------------|
|    Passou     | Resultado observado igual ao esperado          |
|    Falhou     | Divergência → abrir issue `bug` + `fix/<nome>` |
| Não executado | Fora do escopo da Sprint ou bloqueado          |
|   Pendente    | Caso depende de feature ainda não entregue     |

Os resultados por feature ficam na
[Documentação por Feature](features/index.md) e os agregados nos
[Consolidados por Sprint](sprints/index.md).

---
