# Qualidade e Testes

Esta seção reúne a **estratégia de testes** do CrediFab e toda a documentação de
qualidade produzida pela dupla de Qualidade (**Daniel Filipe** e
**Matheus Moretti**) ao longo das Sprints.
--- 

## Nesta seção

| Página                                            | Conteúdo                                                           |
|---------------------------------------------------|--------------------------------------------------------------------|
| [Roteiro de Testes](roteiro-testes.md)            | Casos planejados TS-01 a TS-27 e rastreabilidade com os requisitos |
| [Modelo GQM](gqm.md)                              | Metas, perguntas e métricas (M1-M4) que medem a qualidade          |
| [Resumo de Métricas](resumo-metricas.md)          | Visão executiva de todas as métricas de qualidade coletadas        |
| [Métricas de Produto](metricas-produto.md)        | Métricas de negócio e de experiência do usuário                    |
| [Documentação por Feature](features/index.md)     | Um relatório de teste para cada feature testada                    |
| [Documentação por Tarefa Técnica](tasks/index.md) | Relatórios de QA das tarefas de integração/refatoração             |
| [Documentação por Correção (fix)](fix/index.md)   | Relatórios de QA das correções de defeitos                         |
| [Consolidados por Sprint](sprints/index.md)       | Visão agregada de testes e GQM por Sprint                          |

---
## Estratégia em resumo

A estratégia segue a ideia de **pirâmide de testes**: muitos testes unitários,
menos de integração, menos ainda E2E, e testes de carga no topo.

```
                      ▲   Carga (Locust)
                    ╱  ╲
                 ╱ E2E ╲       Fluxos completos (client Flask)
              ╱───────╲
           ╱  Integração ╲    Endpoints contra SQLite em memória
       ╱──────────────╲
   ╱            Unitários           ╲        Lógica de services e schemas, isolada com mocks
╱─────────────────────╲
```

---
### Tecnologias por nível

| Nível           | Ferramenta                                          | Escopo                                                   |
|-----------------|-----------------------------------------------------|----------------------------------------------------------|
| Unitário        | **Pytest + pytest-mock**                            | Lógica de service isolada com mocks; schemas marshmallow |
| Integração      | **Pytest + client Flask**                           | Endpoints contra **SQLite em memória**                   |
| E2E (API)       | **Pytest + client Flask**                           | Fluxos multi-endpoint encadeados                         |
| Front-end       | **Vitest + React Testing Library**                  | Componentes e telas                                      |
| Carga           | **Locust**                                          | Endpoint de simulação de crédito                         |


---
## Estrutura da suíte (back-end)

```
backend/tests/
  conftest.py                 # fixtures globais (app, client, clean_db, auth…)
  unit/                       # test_company_service.py, test_company_schema.py
  integration/                # test_company_routes.py, test_company_service_db.py
  e2e/                        # onboarding, financeiro, contas e cadastro de empresa
```

Fixtures globais em `conftest.py`: `app` 

---
## Fluxo de Trabalho por Sprint

1. **Início:** alinhar com as duplas de dev os critérios de aceitação testáveis.
2. **Durante:** escrever testes em paralelo ao desenvolvimento.
3. Dev finaliza em `feature/<nome>`; Qualidade cria `test/<feature>` a partir
   dela e escreve/roda os scripts.
4. **Bug encontrado:** abrir issue com label `bug` + escrever teste que o
   reproduz **antes** do fix; correção em `fix/<nome>`; o ciclo recomeça.
5. **Todos passam:** apaga-se `test/`, abre-se PR da feature para `develop`
   (a CI de testes precisa passar).

---
## Documentos de Qualidade Produzidos

| Documento                              | Frequência  | Onde                                              |
|----------------------------------------|-------------|---------------------------------------------------|
| **Documentação de Testes - Feature**   | Por feature | [Documentação por Feature](features/index.md)     |
| **Documentação de Testes - Tarefa**    | Por tarefa  | [Documentação por Tarefa Técnica](tasks/index.md) |
| **Documentação de Testes - Correção**  | Por fix     | [Documentação por Correção (fix)](fix/index.md)   |
| **Consolidado de Testes - Sprint**     | Por Sprint  | [Consolidados por Sprint](sprints/index.md)       |
| **Análise GQM - Sprint**               | Por Sprint  | Dentro de cada consolidado                        |

---
