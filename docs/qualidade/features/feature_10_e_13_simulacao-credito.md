# Documentação de Testes - Simulação de Crédito (Frontend + Backend)

> Relatório **único** da funcionalidade **H - Simulação de Crédito**, que reúne as duas
> US irmãs (separadas apenas por camada no backlog):
> [us10 - frontend](../../issues/us10.md) e [us13 - backend](../../issues/us13.md).
> O código das duas foi integrado em uma branch única a partir da `develop`.

## 1. Identificação

| Campo                         | Valor                                                                           |
|-------------------------------|---------------------------------------------------------------------------------|
| **Feature**                   | Simulação de Crédito (frontend + backend)                                       |
| **US**                        | us10 (frontend) + us13 (backend)                                                |
| **Cenário**                   | CEN-04 - Diagnóstico e simulação de crédito                                     |
| **Requisito**                 | R12                                                                             |
| **Sprint**                    | 9                                                                               |
| **Branch de desenvolvimento** | `feature/10-e-13-simulacao-credito` (integração, a partir da `develop`)         |
| **Branches de origem**        | `feature/10-simulacao-credito` (front) · `feature/13-simulacao-creditos` (back) |
| **PR / Pipeline**             | PR #67 → `develop` · GitHub Actions `tests` (run 27767281384) - **success**     |
| **Responsáveis (QA)**         | Daniel Filipe / Matheus Moretti                                                 |
| **Data**                      | 23/06/2026                                                                      |

## 2. Critérios de aceitação testáveis

### Cálculo (Price / SAC) - backend
- [x] **CA-01** Price gera parcelas de valor igual e o saldo devedor zera ao fim (± R$ 0,01) - `TS-02`, `TS-06`
- [x] **CA-02** Taxa de juros 0: parcela = valor ÷ prazo e juros totais = 0 - `TS-01`
- [x] **CA-03** SAC tem amortização constante, parcelas decrescentes e juros menores que o Price - `TS-03`, `TS-04`, `TS-05`
- [x] **CA-04** `POST /simulations/calculate` retorna o detalhamento **sem gravar** no banco - `TS-12`
- [x] **CA-05** Com empresa, o cálculo anexa a projeção de fluxo de caixa; sem histórico, status "Indisponível" - `TS-07`…`TS-11`

### Persistência e listagem - backend
- [x] **CA-06** `POST /simulations` salva e retorna `simulation_id`; valores calculados no backend - `TS-16`, `TS-17`
- [x] **CA-07** `GET /simulations` lista apenas as simulações da empresa - `TS-18`, `TS-19`
- [x] **CA-08** `DELETE /simulations/<id>` remove da empresa; inexistente retorna 404 - `TS-20`, `TS-21`
- [ ] **CA-09** Exclusão da empresa remove simulações em cascata (`ON DELETE CASCADE`) - relação `cascade='all, delete-orphan'` declarada em `Company`/`User`, mas **não exercitada** por caso de teste dedicado

### Validações e segurança - backend
- [x] **CA-10** Entradas inválidas retornam 400 (modalidade fora de PRICE/SAC, valor ≤ 0) - `TS-13`, `TS-14`
- [x] **CA-11** Taxa de juros 0 é aceita (juros zero) - `TS-01`
- [x] **CA-16** Todos os endpoints exigem autenticação (401 sem token) - `TS-15`

### Frontend
- [x] **CA-12** Parcela, total e juros exibidos em tempo real, sem salvar - `TS-22`, `TS-24`
- [x] **CA-13** Gráfico de evolução (Recharts) e destaque da "1ª Parcela" no SAC - `TS-23` (Recharts stubado no jsdom; rótulo SAC validado)
- [~] **CA-14** Salvar persiste; lista exibe salvas; excluir pede confirmação e cancelar não remove - confirmação/cancelamento OK no componente (`TS-25`…`TS-28`), **mas o fluxo real (salvar/listar) está quebrado** por contrato front↔back → **DEF-01/02/03**
- [ ] **CA-15** Erros da API exibidos de forma amigável sem travar a interface - **não coberto** por caso dedicado

## 3. Casos executados

| Caso  | Descrição                                                          | Nível            | Esperado                              | Observado | Status |
|-------|-------------------------------------------------------------------|------------------|---------------------------------------|-----------|--------|
| TS-01 | `calculate_table_price` com taxa 0                                | Unitário         | parcela = valor/prazo, juros 0        | Conforme  | OK      |
| TS-02 | `calculate_table_price` parcelas iguais, saldo final zera         | Unitário         | parcela constante, saldo ≈ 0          | Conforme  | OK      |
| TS-03 | `calculate_table_sac` amortização constante, saldo zera           | Unitário         | amortização igual, saldo ≈ 0          | Conforme  | OK      |
| TS-04 | `calculate_table_sac` parcelas decrescentes                       | Unitário         | parcelas em ordem decrescente         | Conforme  | OK      |
| TS-05 | SAC paga menos juros que o Price (mesmos parâmetros)              | Unitário         | juros SAC < juros Price               | Conforme  | OK      |
| TS-06 | `process_simulation` Price - resumo coerente                      | Unitário         | total_juros = total − valor, 12 parc. | Conforme  | OK      |
| TS-07 | `process_simulation` sem `company_id` não projeta fluxo           | Unitário         | sem `projecao_fluxo_caixa`            | Conforme  | OK      |
| TS-08 | `process_simulation` com `company_id` anexa projeção              | Unitário         | inclui projeção (status "Indisponível")| Conforme  | OK      |
| TS-09 | `project_impact_cash_flow` sem transações                         | Unitário         | status "Indisponível", `perc` None    | Conforme  | OK      |
| TS-10 | `project_impact_cash_flow` empresa lucrativa                      | Unitário         | status "Saudável", perc definido      | Conforme  | OK      |
| TS-11 | `project_impact_cash_flow` empresa no prejuízo                    | Unitário         | status "Alerta vermelho", perc 100    | Conforme  | OK      |
| TS-12 | `POST /simulations/calculate` Price não persiste                  | Integração       | `200` + detalhamento, lista vazia     | Conforme  | OK      |
| TS-13 | `POST /simulations/calculate` modalidade inválida                 | Integração       | `400`                                 | Conforme  | OK      |
| TS-14 | `POST /simulations/calculate` valor negativo                      | Integração       | `400`                                 | Conforme  | OK      |
| TS-15 | `POST /simulations/calculate` sem token                           | Integração       | `401`                                 | Conforme  | OK      |
| TS-16 | `POST /simulations/` salva a simulação                            | Integração       | `201` + `simulation_id`               | Conforme  | OK      |
| TS-17 | `POST /simulations/` sem `company_id`                             | Integração       | `400`                                 | Conforme  | OK      |
| TS-18 | `GET /simulations` lista da empresa                               | Integração       | `200` + 2 simulações                  | Conforme  | OK      |
| TS-19 | `GET /simulations` sem `company_id`                               | Integração       | `400`                                 | Conforme  | OK      |
| TS-20 | `DELETE /simulations/<id>` existente                              | Integração       | `200`, some da lista                  | Conforme  | OK      |
| TS-21 | `DELETE /simulations/<id>` inexistente                            | Integração       | `404`                                 | Conforme  | OK      |
| TS-22 | Cálculo em tempo real (parcela, total, juros)                     | Unitário (front) | resultado exibido sem salvar          | Conforme  | OK      |
| TS-23 | Modalidade SAC destaca a "1ª Parcela"                             | Unitário (front) | rótulo "1ª Parcela" aparece           | Conforme  | OK      |
| TS-24 | Formulário incompleto não exibe resultado                         | Unitário (front) | sem "Total a Pagar"                   | Conforme  | OK      |
| TS-25 | Salvar chama o serviço de persistência                            | Unitário (front) | serviço chamado 1×                    | Conforme  | OK      |
| TS-26 | Lista simulações salvas com seus parâmetros                       | Unitário (front) | linha com modalidade/valor            | Conforme  | OK      |
| TS-27 | Excluir pede confirmação; "Cancelar" não chama o serviço          | Unitário (front) | serviço não chamado; modal fecha      | Conforme  | OK      |
| TS-28 | Excluir confirmado chama o serviço com o id                       | Unitário (front) | serviço chamado com o id              | Conforme  | OK      |

> **Observação importante:** os casos de front (`TS-22`…`TS-28`) são testes de componente
> (Vitest) com o **serviço da API e o Recharts mockados**. Por isso passam mesmo com os
> defeitos de contrato **DEF-01/02/03** - que só apareceriam num teste end-to-end (não há
> E2E de front nesta feature).

## 4. Evidências

Execução pela **pipeline** (GitHub Actions, workflow `tests`, run `27767281384`, PR #67),
artefatos em `testes/relatorio-backend/` e `testes/relatorio-frontend/`.

### Backend - `pytest` (Python 3.14.5, 188 itens)

```
tests/unit/feature_10_13/test_simulation_service.py ......... (11 passed)
tests/integration/feature_10_13/test_simulation_endpoints.py .......... (10 passed)
...
===== 6 failed, 168 passed, 13 xfailed, 1 xpassed, 246 warnings in 36.12s ======
```

- **Os 21 testes da simulação (11 unit + 10 integração) passaram.**
- As **6 falhas** são **pré-existentes e fora do escopo** desta feature - todas em
  `feature_6` (transações): `create/update/delete_transaction()` com assinatura divergente
  do teste (`current_user_id` / `company_id`) e `ProgrammingError: type 'dict' is not
  supported` na edição. Devem ser tratadas no relatório da feature 6.

### Frontend - `vitest run --coverage`

```
src/pages/Simulacoes/Simulacoes.test.jsx (7 tests) 1072ms
 Test Files  8 passed (8)
      Tests  49 passed | 3 skipped (52)
```

## 5. Defeitos encontrados

| ID     | Descrição                                                                                                                                                                                                                                                                                              | Branch de correção            | Status |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|--------|
| DEF-01 | **Contrato de salvar quebrado.** O front (`simulacao.service.js` / `Simulacoes.jsx#handleSalvar`) envia `{ valor_solicitado, prazo_meses, modalidade, taxa_juros, valor_parcela, valor_total, total_juros, id_empresa }`, mas o `SimulationSaveDTO` exige `{ requested_amount, deadline_month, interest_rate, modality, company_id }` (e rejeita campos extras). Resultado: salvar real retorna **400**. Não pega nos testes porque o serviço é mockado no front. | `fix/simulacao-contrato-salvar` | Aberto |
| DEF-02 | **Listagem sempre vazia.** O backend (`GET /simulations`) responde `{ "simulations": [...] }`, mas o front lê `dados.simulacoes` (`Simulacoes.jsx#carregarSimulacoes`). Como a chave não bate, a lista de simulações salvas fica **sempre vazia** na tela.                                              | `fix/simulacao-contrato-listar` | Aberto |
| DEF-03 | **Campo de id divergente na listagem.** O backend devolve `simulation_id` por item, mas o front usa `sim.id_simulacao` (key da linha e parâmetro do excluir). Mesmo corrigido o DEF-02, a exclusão chamaria o serviço com `undefined`.                                                                  | `fix/simulacao-contrato-id`     | Aberto |
| DEF-04 | **Mensagem de sucesso nunca aparece (UX, menor).** Em `handleSalvar`, `setMensagemSalvo(...)` e `setForm(FORM_INICIAL)` ocorrem juntos; o reset zera o `resumo`, desmontando o bloco `{resumo && (…)}` que contém a `<p class="msg-success">`. A confirmação de "Simulação salva" não chega a ser exibida. | `fix/simulacao-msg-sucesso`     | Aberto |

> Nota: o defeito de relação ORM da antiga `feature/10` (`Company` sem a propriedade
> `simulations`) **não ocorre** nesta integração - `Company`/`User` passaram a declarar a
> relação inversa com `Simulation`, e os 10 testes de integração configuram os mappers sem erro.

## 6. Cobertura

### Backend - `coverage.xml` (artefato da pipeline)

| Módulo                               | Cobertura (linhas) |
|--------------------------------------|--------------------|
| `app/routes/simulation_routes.py`    | **97,7%**          |
| `app/models/simulation.py`           | **94,7%**          |
| `app/schemas/simulation_schema.py`   | **93,8%**          |
| `app/services/simulation_service.py` | **92,7%**          |

### Frontend - `coverage/` (artefato da pipeline)

| Módulo                                                | Cobertura (linhas) | Observação                                                                 |
|-------------------------------------------------------|--------------------|----------------------------------------------------------------------------|
| `src/pages/Simulacoes/ConfirmacaoExclusaoSimulacao.jsx`| **100%**           | exercitado por `TS-27`/`TS-28`                                             |
| `src/pages/Simulacoes/Simulacoes.jsx`                 | **68,8%**          | não cobertos: bloco de projeção/gráfico de fluxo de caixa (depende de `fetch`) e ramos de erro |
| `src/pages/Simulacoes/` (pasta)                       | **70,2%**          | acima da meta de **≥ 60%**                                                 |
| `src/services/simulacao.service.js`                   | **0%**             | mockado nos testes de componente (padrão dos services do projeto)         |

Backend e o núcleo da UI ficam acima da meta de **≥ 60%**.

## 7. Parecer final

**Aprovada com pendências.**

As **duas camadas funcionam individualmente e estão verdes**: o cálculo Price/SAC, o resumo,
a projeção de fluxo de caixa e os endpoints REST passam nos 21 testes de backend (cobertura
92-98%); a UI calcula em tempo real, destaca a 1ª parcela no SAC e trata a confirmação de
exclusão (7 testes de front verdes). A pipeline do PR #67 fechou **verde** e o defeito de
ORM da branch antiga foi resolvido na integração.

As pendências registradas são de **contrato front↔back** (não capturadas pelos testes por
camada, pois o serviço do front é mockado e não há E2E) e serão **resolvidas na etapa de
integração**, sem bloquear a entrega das camadas:

- **DEF-01** - salvar envia o payload em formato diferente do `SimulationSaveDTO` → 400 (CA-06/CA-14).
- **DEF-02** - listagem lê a chave errada da resposta → lista vazia (CA-07/CA-14).
- **DEF-03** - id divergente (`simulation_id` × `id_simulacao`) na listagem/exclusão (CA-08).
- **DEF-04** - UX menor: mensagem de sucesso ao salvar nunca aparece.

**Pendências para a integração / próxima iteração:**
1. Alinhar o contrato (DEF-01/02/03): padronizar nomes de campos e a chave de resposta entre
   `simulacao.service.js`/`Simulacoes.jsx` e o `SimulationSaveDTO`/`get_simulation`
   (decidir um lado como fonte da verdade - sugestão: o contrato do backend).
2. **DEF-04** - preservar a mensagem de sucesso fora do bloco `{resumo && …}`.
3. Adicionar um caso cobrindo **CA-09** (cascade na exclusão da empresa) e **CA-15** (erros
   de API amigáveis), hoje sem teste dedicado.
