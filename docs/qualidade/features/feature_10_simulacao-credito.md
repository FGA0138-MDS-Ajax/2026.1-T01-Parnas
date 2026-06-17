# Relatório de QA — Feature 10: Simulação de Crédito

## 1. Identificação

| Campo                          | Valor                               |
|--------------------------------|-------------------------------------| 
| **Feature**                    | Simulação de Crédito                |
| **Cenário**                    |                                     |
| **Requisito**                  | — (não especificado na issue)       |
| **Sprint**                     | — (não identificada)                |
| **Branch de desenvolvimento**  | `feature/10-simulacao-credito`      |
| **Branch de teste (QA)**       | `test/feature/10-simulacao-credito` |
| **Responsáveis (QA)**          | Daniel Filipe / Matheus Moretti     |
| **Data**                       | 17/06/2026                          |

## 2. Critérios de aceitação testáveis

- [x] **CA-01** Price gera parcelas de valor igual e o saldo devedor zera ao fim (± R$ 0,01) — `TS-02`
- [x] **CA-02** Taxa de juros 0: parcela = valor ÷ prazo e juros totais = 0 — `TS-01`
- [x] **CA-03** SAC tem amortização constante, parcelas decrescentes e juros menores que o Price — `TS-03`, `TS-04`, `TS-06`
- [ ] **CA-04** `POST /simulacoes/calcular` retorna detalhamento **sem gravar** — lógica verde no unitário (`TS-05`), mas o **endpoint é inacessível** → ver **DEF-01** (`TS-12`)
- [x] **CA-05** Com empresa, o cálculo anexa a projeção de fluxo de caixa; sem histórico, status "Indisponível" — `TS-08`, `TS-09` (lógica coberta no unitário)
- [ ] **CA-06** `POST /simulacoes` salva e retorna `id_simulacao`; valores calculados no backend — **endpoint inacessível** → **DEF-01** (`TS-17`)
- [ ] **CA-07** `GET /simulacoes` lista apenas as simulações da empresa — **endpoint inacessível** → **DEF-01** (`TS-19`)
- [ ] **CA-08** `DELETE /simulacoes/<id>` remove da empresa; inexistente retorna 404 — **endpoint inacessível** → **DEF-01** (`TS-21`, `TS-22`)
- [ ] **CA-09** Exclusão da empresa remove simulações em cascata (`ON DELETE CASCADE`) — **não verificado** (bloqueado por **DEF-01**; o SQLite de teste não força FK por padrão)
- [ ] **CA-10** Entradas inválidas retornam 400 (modalidade fora de PRICE/SAC, valor ≤ 0, prazo ≤ 0) — validação de schema **não exercitável** pelos endpoints → **DEF-01** (`TS-14`, `TS-15`)
- [x] **CA-11** Taxa de juros 0 é aceita (juros zero) — `TS-01`
- [x] **CA-12** Parcela, total e juros exibidos em tempo real, sem salvar — `TS-23`
- [x] **CA-13** Gráfico de evolução (Recharts) e destaque da "1ª Parcela" no SAC — `TS-24` (Recharts stubado em jsdom; rótulo SAC validado)
- [x] **CA-14** Salvar persiste; lista exibe salvas; excluir pede confirmação e cancelar não remove — `TS-26`, `TS-27`, `TS-28`, `TS-29`
- [ ] **CA-15** Erros da API exibidos de forma amigável sem travar — **não coberto** por caso de teste dedicado

## 3. Casos executados

| Caso  | Descrição                                                    | Nível      | Esperado                                 | Observado                | Status |
|-------|--------------------------------------------------------------|------------|------------------------------------------|--------------------------|--------|
| TS-01 | `calculate_table_price` sem juros (taxa 0)                   | Unitário   | parcela = valor/prazo, juros 0           | Conforme                 | ✅      |
| TS-02 | `calculate_table_price` parcelas iguais e saldo final zerado | Unitário   | parcela constante, saldo ≈ 0             | Conforme                 | ✅      |
| TS-03 | `calculate_table_sac` amortização constante                  | Unitário   | amortização igual, saldo ≈ 0             | Conforme                 | ✅      |
| TS-04 | `calculate_table_sac` parcelas decrescentes                  | Unitário   | parcelas em ordem decrescente            | Conforme                 | ✅      |
| TS-05 | `process_simulation` Price — resumo coerente                 | Unitário   | total_juros = total − valor, 12 parcelas | Conforme                 | ✅      |
| TS-06 | `process_simulation` SAC paga menos juros que o Price        | Unitário   | juros SAC < juros Price                  | Conforme                 | ✅      |
| TS-07 | `process_simulation` sem `company_id` não projeta fluxo      | Unitário   | sem chave `projecao_fluxo_caixa`         | Conforme                 | ✅      |
| TS-08 | `process_simulation` com `company_id` inclui projeção        | Unitário   | anexa projeção (status "Indisponível")   | Conforme                 | ✅      |
| TS-09 | `project_impact_cash_flow` sem transações                    | Unitário   | status "Indisponível", `perc` None       | Conforme                 | ✅      |
| TS-10 | `project_impact_cash_flow` empresa lucrativa                 | Unitário   | status "Saudável", comprometimento 12,5% | Conforme                 | ✅      |
| TS-11 | `project_impact_cash_flow` empresa no prejuízo               | Unitário   | status "Alerta Vermelho", perc 100       | Conforme                 | ✅      |
| TS-12 | `POST /api/simulations/calculate` Price não persiste         | Integração | `200` + detalhamento, lista vazia        | `InvalidRequestError`    | ❌      |
| TS-13 | `POST /api/simulations/calculate` SAC retorna detalhamento   | Integração | `200` + modalidade SAC                   | `InvalidRequestError`    | ❌      |
| TS-14 | `POST /api/simulations/calculate` modalidade inválida        | Integração | `400`                                    | `InvalidRequestError`    | ❌      |
| TS-15 | `POST /api/simulations/calculate` valor negativo             | Integração | `400`                                    | `InvalidRequestError`    | ❌      |
| TS-16 | `POST /api/simulations/calculate` sem token                  | Integração | `401`                                    | Conforme                 | ✅      |
| TS-17 | `POST /api/simulations/` salva a simulação                   | Integração | `201` + `id_simulacao`                   | `InvalidRequestError`    | ❌      |
| TS-18 | `POST /api/simulations/` sem `company_id`                    | Integração | `400`                                    | `InvalidRequestError`    | ❌      |
| TS-19 | `GET /api/simulations` lista da empresa                      | Integração | `200` + 2 simulações                     | `InvalidRequestError`    | ❌      |
| TS-20 | `GET /api/simulations` sem `company_id`                      | Integração | `400`                                    | `InvalidRequestError`    | ❌      |
| TS-21 | `DELETE /api/simulations/<id>` existente                     | Integração | `200`, some da lista                     | `InvalidRequestError`    | ❌      |
| TS-22 | `DELETE /api/simulations/<id>` inexistente                   | Integração | `404`                                    | `InvalidRequestError`    | ❌      |
| TS-23 | Cálculo em tempo real (parcela, total, juros)                | Unitário   | resultado exibido sem salvar             | Conforme                 | ✅      |
| TS-24 | Modalidade SAC destaca a "1ª Parcela"                        | Unitário   | rótulo "1ª Parcela" aparece              | Conforme                 | ✅      |
| TS-25 | Formulário incompleto não exibe resultado                    | Unitário   | sem "Total a Pagar"                      | Conforme                 | ✅      |
| TS-26 | Salvar envia parâmetros + resumo calculado e limpa o form    | Unitário   | serviço chamado; campos resetados        | Conforme                 | ✅      |
| TS-27 | Lista simulações salvas com data e parâmetros                | Unitário   | linha com modalidade, prazo, etc.        | Conforme                 | ✅      |
| TS-28 | Exclui simulação após confirmação                            | Unitário   | serviço chamado com o id                 | Conforme                 | ✅      |
| TS-29 | Cancelar exclusão não chama o serviço                        | Unitário   | serviço não chamado; modal fecha         | Conforme                 | ✅      |

> Os casos `TS-23` a `TS-29` são testes de componente (front, Vitest) — unitários de
> UI com o serviço e o Recharts mockados.

## 4. Evidências

### Backend — unitário — `python -m pytest tests/unit/feature_10 -v`

```
tests/unit/feature_10/test_simulation_service.py::test_calculate_table_price_sem_juros PASSED
tests/unit/feature_10/test_simulation_service.py::test_calculate_table_price_parcelas_iguais PASSED
tests/unit/feature_10/test_simulation_service.py::test_calculate_table_sac_amortizacao_constante PASSED
tests/unit/feature_10/test_simulation_service.py::test_calculate_table_sac_parcelas_decrescentes PASSED
tests/unit/feature_10/test_simulation_service.py::test_process_simulation_price_resumo_coerente PASSED
tests/unit/feature_10/test_simulation_service.py::test_process_simulation_sac_juros_menor_que_price PASSED
tests/unit/feature_10/test_simulation_service.py::test_process_simulation_sem_company_id_nao_projeta_fluxo PASSED
tests/unit/feature_10/test_simulation_service.py::test_process_simulation_com_company_id_inclui_projecao PASSED
tests/unit/feature_10/test_simulation_service.py::test_project_impact_cash_flow_sem_transacoes PASSED
tests/unit/feature_10/test_simulation_service.py::test_project_impact_cash_flow_empresa_lucrativa PASSED
tests/unit/feature_10/test_simulation_service.py::test_project_impact_cash_flow_empresa_no_prejuizo PASSED
============================== 11 passed in 0.04s ==============================
```

### Backend — integração — `python -m pytest tests/integration/feature_10 -v`

```
tests/integration/feature_10/test_simulation_endpoints.py::test_calcular_price_nao_persiste ERROR
tests/integration/feature_10/test_simulation_endpoints.py::test_calcular_sac_retorna_detalhamento ERROR
tests/integration/feature_10/test_simulation_endpoints.py::test_calcular_modalidade_invalida ERROR
tests/integration/feature_10/test_simulation_endpoints.py::test_calcular_valor_negativo ERROR
tests/integration/feature_10/test_simulation_endpoints.py::test_calcular_exige_autenticacao PASSED
tests/integration/feature_10/test_simulation_endpoints.py::test_salvar_simulacao ERROR
tests/integration/feature_10/test_simulation_endpoints.py::test_salvar_sem_company_id ERROR
tests/integration/feature_10/test_simulation_endpoints.py::test_listar_simulacoes_da_empresa ERROR
tests/integration/feature_10/test_simulation_endpoints.py::test_listar_sem_company_id ERROR
tests/integration/feature_10/test_simulation_endpoints.py::test_excluir_simulacao_existente ERROR
tests/integration/feature_10/test_simulation_endpoints.py::test_excluir_simulacao_inexistente ERROR

E   sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize -
    Triggering mapper: 'Mapper[Simulation(simulation)]'. Original exception was:
    Mapper 'Mapper[Company(company)]' has no property 'simulations'.
========================= 1 passed, 10 errors in 4.86s =========================
```

> O único caso de integração verde (`TS-16`) é o de autenticação: o `401` do JWT é
> retornado **antes** de qualquer acesso ao banco, então não chega a disparar a
> configuração dos mappers que falha (**DEF-01**). Todos os demais erram no setup.

### Frontend — `npx vitest run src/pages/Simulacoes/Simulacoes.test.jsx`

```
 ✓ src/pages/Simulacoes/Simulacoes.test.jsx (7 tests) 434ms
 Test Files  1 passed (1)
      Tests  7 passed (7)
```

**Total:** 29 testes — **19 passaram, 10 em erro** (todos documentando **DEF-01**), 0 skip.

## 5. Defeitos encontrados

| ID     | Descrição                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Status |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| DEF-01 | No model `backend/app/models/simulation.py`, `Simulation.company` usa `back_populates='simulations'`, mas `Company` (`backend/app/models/company.py`) **não declara** essa relação → `InvalidRequestError: Mapper 'Company' has no property 'simulations'` ao configurar os mappers. **Impacto:** toda a persistência da feature (salvar, listar, excluir) fica **inacessível**, e como o registry de mappers é global, importar o model **contamina o restante da suíte** — no `pytest` completo, a inicialização do app derruba também os testes de integração das features 2, 7 e 14. Confirmado via `configure_mappers()` e pelos 10 testes de integração em erro. | Aberto |
| DEF-02 | Em `frontend/src/pages/Simulacoes/Simulacoes.jsx`, `handleSalvar` faz `setMensagemSalvo('Simulação salva com sucesso!')` e `setForm(FORM_INICIAL)` na mesma ação. O reset zera o `resumo`, desmontando o bloco `{resumo && (…)}` que contém a `<p class="msg-success">` — a mensagem de sucesso **nunca chega a ser exibida** ao usuário. Severidade menor (UX).                                                                                                                                                                                                                                                                                                       | Aberto |

> Nota (fora do escopo desta feature): a suíte de integração completa também acusa
> vermelhos **pré-existentes** em outras features (ex.: `feature_2/test_login_email_inexistente`
> e `feature_14/test_calcular_exige_autenticacao` → `404` em vez de `401`), além da
> contaminação descrita no DEF-01. Devem ser tratados nos relatórios das respectivas
> features.

## 6. Cobertura

**Backend** — `pytest tests/unit/feature_10 --cov=app.services.simulation_service --cov-report=term-missing`

| Módulo                               | Cobertura | Observação                                                                                                                                                                                                                                                                                       |
|--------------------------------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `app/services/simulation_service.py` | **70%**   | Cálculo Price/SAC, `process_simulation` e projeção de fluxo de caixa totalmente cobertos. As linhas não cobertas (116–169) são `save_simulation`, `get_simulation` e `delete_simulation` — funções que tocam o banco e que **só seriam exercitáveis via integração**, bloqueada pelo **DEF-01**. |

**Frontend** — `npx vitest run src/pages/Simulacoes/Simulacoes.test.jsx --coverage`

| Módulo                                | Cobertura (linhas) | Observação                                                                                                                                                     |
|---------------------------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `src/pages/Simulacoes/Simulacoes.jsx` | **68,8%**          | Não cobertos: o bloco de projeção/gráfico de fluxo de caixa (depende de `fetch` de transações, fora do escopo desta feature) e ramos de erro de salvar/listar. |
| Pasta `src/pages/Simulacoes/`         | **70,2%**          | Inclui `ConfirmacaoExclusaoSimulacao.jsx`, exercitado pelos `TS-28`/`TS-29`.                                                                                   |

A lógica de negócio (cálculo + projeção) e o núcleo da UI estão acima da meta de **≥ 60%**.

## 7. Parecer final

**Reprovada.**

A lógica de negócio está coberta e verde: cálculo pela Tabela Price (parcelas
iguais, saldo zerado), SAC (amortização constante, parcelas decrescentes, juros
menores que o Price), resumo consolidado e projeção de impacto no fluxo de caixa
(service relevante coberto). A interface está verde — cálculo em tempo real,
destaque da 1ª parcela no SAC, salvar, listar, excluir com confirmação e cancelar.

**Porém a feature não é entregável como está**, por causa de um defeito de produção
crítico:

- **DEF-01** — o model `Simulation` referencia uma relação `simulations` inexistente
  em `Company`, quebrando a configuração dos mappers do SQLAlchemy. Isso torna
  **toda a camada de persistência da simulação inacessível** (salvar/listar/excluir)
  e **contamina o restante da suíte de integração** do backend (features 2, 7 e 14).
- **DEF-02** — defeito menor de UX: a mensagem de sucesso ao salvar nunca aparece,
  pois o reset do formulário desmonta o painel que a contém.

**Próximos passos para reavaliação:**
1. **DEF-01** — declarar em `Company` a relação inversa, p.ex.:
   `simulations = db.relationship('Simulation', back_populates='company', cascade='all, delete-orphan')`
   (isso também viabiliza o CASCADE DELETE de **CA-09**).
2. **DEF-02** — preservar a mensagem de sucesso fora do bloco `{resumo && …}` (ou não
   resetar o resumo no salvar).
