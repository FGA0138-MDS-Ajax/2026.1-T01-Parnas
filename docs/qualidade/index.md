# Qualidade e Testes

Esta seção reúne a **estratégia de testes** do CrediFab e toda a documentação de
qualidade produzida pela dupla de Qualidade (**Daniel Filipe** e
**Matheus Moretti**) ao longo das Sprints.
--- 

## Nesta seção

| Página | Conteúdo |
| --- | --- |
| [Roteiro de Testes](roteiro-testes.md) | Casos planejados TS-01 a TS-14 e rastreabilidade com os requisitos |
| [Modelo GQM](gqm.md) | Metas, perguntas e métricas (M1–M4) que medem a qualidade |
| [Documentação por Feature](features/index.md) | Um relatório de teste para cada feature testada |
| [Consolidados por Sprint](sprints/index.md) | Visão agregada de testes e GQM por Sprint |

---
## Estratégia em resumo

A estratégia segue a ideia de **pirâmide de testes**: muitos testes unitários,
menos de integração, menos ainda E2E, e testes de carga sob demanda.

```
                      ▲   Carga (sob demanda — Locust)
                    ╱  ╲
                 ╱ E2E ╲       Fluxos completos (Playwright)
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
| E2E (navegador) | **Playwright** *(a configurar)*                     | CEN-01 a CEN-04, caminhos felizes                        |
| Front-end       | **Vitest + React Testing Library** *(a configurar)* | Componentes e telas                                      |
| Carga           | **Locust** *(sob demanda)*                          | Endpoint de simulação de crédito (futuro)                |


---
## Estrutura da suíte (back-end)

```
backend/tests/
  conftest.py                 # fixtures globais (app, client, clean_db, auth…)
  unit/                       # test_company_service.py, test_company_schema.py
  integration/                # test_company_routes.py, test_company_service_db.py
  e2e/                        # test_company_registration_flow.py
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
   (a CI deve passar — quando existir).

---
## Documentos de Qualidade Produzidos

| Documento                            | Frequência  | Onde                                            |
|--------------------------------------|-------------|-------------------------------------------------|
| **Documentação de Testes — Feature** | Por feature | [Documentação por Feature](features/index.md)   |
| **Consolidado de Testes — Sprint**   | Por Sprint  | [Consolidados por Sprint](sprints/index.md)     |
| **Análise GQM — Sprint**             | Por Sprint  | Dentro de cada consolidado                      |

---
