# Documentação de Testes — Simulação de Crédito (Frontend + Backend)

> Relatório **único** da funcionalidade **H — Simulação de Crédito**, que reúne as duas
> US irmãs (separadas apenas por camada no backlog):
> [us10 — frontend](../../issues/us10.md) e [us13 — backend](../../issues/us13.md).
> O código das duas foi integrado em uma branch única a partir da `develop`.

## 1. Identificação

| Campo                          | Valor                                                       |
|--------------------------------|-------------------------------------------------------------|
| **Feature**                    | Simulação de Crédito (frontend + backend)                   |
| **US**                         | us10 (frontend) + us13 (backend)                            |
| **Cenário**                    | CEN-04 — Diagnóstico e simulação de crédito                 |
| **Requisito**                  | R12                                                         |
| **Sprint**                     | 9                                                           |
| **Branch de desenvolvimento**  | `feature/10-e-13-simulacao-credito` (integração, a partir da `develop`) |
| **Branches de origem**         | `feature/10-simulacao-credito` (front) · `feature/13-simulacao-creditos` (back) |
| **Branch de teste (QA)**       | `test/feature/10-e-13-simulacao-credito`                    |
| **Responsáveis (QA)**          | Daniel Filipe / Matheus Moretti                             |
| **Data**                       | —                                                           |

## 2. Critérios de aceitação testáveis

### Cálculo (Price / SAC) — backend
- [ ] **CA-01** Price gera parcelas de valor igual e o saldo devedor zera ao fim (± R$ 0,01)
- [ ] **CA-02** Taxa de juros 0: parcela = valor ÷ prazo e juros totais = 0
- [ ] **CA-03** SAC tem amortização constante, parcelas decrescentes e juros menores que o Price
- [ ] **CA-04** `POST /simulacoes/calcular` retorna o detalhamento **sem gravar** no banco
- [ ] **CA-05** Com empresa, o cálculo anexa a projeção de fluxo de caixa; sem histórico, status "Indisponível"

### Persistência e listagem — backend
- [ ] **CA-06** `POST /simulacoes` salva e retorna `id_simulacao`; valores calculados no backend
- [ ] **CA-07** `GET /simulacoes` lista apenas as simulações da empresa
- [ ] **CA-08** `DELETE /simulacoes/<id>` remove da empresa; inexistente retorna 404
- [ ] **CA-09** Exclusão da empresa remove simulações em cascata (`ON DELETE CASCADE`)

### Validações e segurança — backend
- [ ] **CA-10** Entradas inválidas retornam 400 (modalidade fora de PRICE/SAC, valor ≤ 0, prazo ≤ 0)
- [ ] **CA-11** Taxa de juros 0 é aceita (juros zero)
- [ ] **CA-16** Todos os endpoints exigem autenticação (401 sem token)

### Frontend
- [ ] **CA-12** Parcela, total e juros exibidos em tempo real, sem salvar
- [ ] **CA-13** Gráfico de evolução (Recharts) e destaque da "1ª Parcela" no SAC
- [ ] **CA-14** Salvar persiste; lista exibe salvas; excluir pede confirmação e cancelar não remove
- [ ] **CA-15** Erros da API exibidos de forma amigável sem travar a interface

## 3. Casos executados

> **A preencher** após a execução dos testes na branch de integração e da pipeline.

## 4. Evidências

> **A preencher** (saída de `pytest` back + `vitest` front e relatório da pipeline).

## 5. Defeitos encontrados

> **A preencher.** Nota: o defeito de relação ORM da antiga `feature/10` (`Company` sem a
> propriedade `simulations`) foi resolvido na integração — `Company`/`User` passam a
> declarar a relação inversa com `Simulation`.

## 6. Cobertura

> **A preencher.**

## 7. Parecer final

> **A preencher** após a pipeline.
