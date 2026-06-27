# Documentação de Teste - Refatoração: Contas e Transações (fix1 e fix2)

## 1. Identificação

| Campo                           | Valor                                                                        |
|---------------------------------|------------------------------------------------------------------------------|
| **Tarefa**                      | Refatoração das páginas de Contas e Transações (frontend)                    |
| **Issues atendidas**            | `fix1` (integração de Transações) e `fix2` (diferenciação Contas/Transações) |
| **Escopo deste relatório**      | Somente frontend (componentes, hooks e testes)                               |
| **Branch de desenvolvimento**   | `refactor/contas-transacoes`                                                 |
| **Branch base comparada**       | `develop`                                                                    |
| **Sprint**                      | 10                                                                           |
| **Responsáveis (QA)**           | Daniel Filipe / Matheus Moretti                                              |
| **Data**                        | 21/06/2026                                                                   |
| **Evidências**                  | Pipeline CI - job `frontend` (artifact `relatorio-frontend`)                 |
| **Parecer**                     | **APROVADA** (ver §6)                                                        |

---

## 2. Escopo e fronteira do relatório

A refatoração resolve, no **frontend**, os dois problemas mapeados:

- **fix2 - Diferenciação Contas/Transações:** as telas deixaram de ser ambíguas.
  `Contas/` passou a separar **Pendentes** e **Quitadas** (com vencimento, quitar,
  editar e excluir); `Transacoes/` virou o histórico de movimentações; nasceu a
  tela `ContasCaixa/` e os layouts ficaram visualmente distintos.
- **fix1 - Transações:** a aba foi reorganizada e modularizada (novos componentes
  `Finance/`, hooks e utils), com loading, erro e `id_empresa` do contexto já no
  lugar.

A avaliação se restringe ao **job `frontend`** da pipeline, que o GitHub Actions
aprovou (verde). O job de backend está fora do escopo desta entrega.

> A camada de dados ainda usa mock (`useContas`/`useTransacoes`); a troca por API
> real e as regras de backend de cada issue dependem do backend e seguem como
> tarefas das próprias issues `fix1`/`fix2`.

---

## 3. Casos executados (frontend)

Suíte Vitest + Testing Library (`npm run test:coverage`). **93 testes em 18
arquivos, 0 falhas.** Abaixo, os casos das áreas refatoradas.

| Caso  | Descrição                                                             | Nível      | Esperado                                    | Status |
|-------|-----------------------------------------------------------------------|------------|---------------------------------------------|:------:|
| TS-01 | formatCurrency formata BRL (positivo, zero, ausente, negativo)        | Unitário   | Saída `R$` correta                          | Passou |
| TS-02 | formatDate converte ISO para dd/mm/aaaa e trata vazio/nulo            | Unitário   | Conversão e fallback corretos               | Passou |
| TS-03 | useAppliedFilters separa rascunho de aplicado, aplica e limpa         | Unitário   | Estado de filtros consistente               | Passou |
| TS-04 | useContas separa pendentes e quitadas                                 | Unitário   | 5 pendentes / 2 quitadas                    | Passou |
| TS-05 | useContas soma os totais pendentes por tipo                           | Unitário   | Receitas e despesas corretas                | Passou |
| TS-06 | useContas quitar move a conta de pendentes para quitadas              | Integração | Conta sai de pendentes                      | Passou |
| TS-07 | useContas excluir conta pendente remove da lista                      | Integração | Lista atualizada                            | Passou |
| TS-08 | useContas excluir conta quitada falha e registra erro                 | Integração | Regra respeitada, erro setado               | Passou |
| TS-09 | ModalConta valida obrigatórios e salva quando válido                  | Unitário   | Erros corretos / onSalvar chamado           | Passou |
| TS-10 | Página Contas separa Pendentes e Quitadas e oculta ações de quitada   | Unitário   | Seções e regras de ação corretas            | Passou |
| TS-11 | ContasCaixa lista, adiciona e bloqueia nome vazio                     | Unitário   | CRUD em memória consistente                 | Passou |
| TS-12 | ModalTransacao valida movimentação e converte valor/categoria         | Unitário   | onSalvar com tipos corretos                 | Passou |
| TS-13 | ModalTransacao barra data futura                                      | Unitário   | Erro de data, sem salvar                    | Passou |
| TS-14 | ModalTransacao (transferência) exige origem e destino diferentes      | Unitário   | Erro de origem=destino                      | Passou |
| TS-15 | Página Transações lista histórico e aplica filtros/totais             | Unitário   | Render consistente                          | Passou |

> Os demais testes da suíte (Login, Register, Categorias, Dashboard, Documentos,
> Configuracoes, EsqueciSenha, RedefinirSenha, useTransacoes) também passaram,
> completando os 93.

---

## 4. Evidências

Job `frontend` da pipeline (`npm run test:coverage`):

```
 Test Files  18 passed (18)
      Tests  93 passed (93)
```

Comando reproduzível localmente (a partir de `frontend/`):

```bash
npm ci
npm run test:run
```

---

## 5. Cobertura (frontend - módulos refatorados)

| Módulo                         | % Stmts | % Branch |
|--------------------------------|:-------:|:--------:|
| `components/Finance/*`         | 100     | 100      |
| `hooks/useAppliedFilters.js`   | 100     | 100      |
| `pages/Contas/Usecontas.jsx`   | 91.79   | 66.00    |
| `pages/Contas/Contas.jsx`      | 88.85   | 51.61    |
| `pages/Contas/Modalconta.jsx`  | 93.96   | 82.05    |
| `pages/ContasCaixa/*`          | 100     | 100      |
| `pages/Transacoes/ModalTransacao.jsx` | 93.14 | 78.48 |
| `pages/Transacoes/Transacoes.jsx`     | 82.25 | 63.63 |
| `utils/formatCurrency.js`      | 100     | 100      |
| `utils/formatDate.js`          | 100     | 100      |

> Total do projeto: 59.03% de linhas - puxado para baixo por módulos fora do
> escopo (Comparacoes, Relatorios, Simulacoes, `services/`), sem teste.

---

## 6. Parecer final

**APROVADA.**

A refatoração é **somente de frontend** e está íntegra: o job `frontend` da
pipeline passou no GitHub Actions, com **93 testes verdes** e boa cobertura nos
módulos refatorados. No frontend, ela resolve os dois problemas: separa de vez
**Contas** e **Transações** (fix2) e reorganiza a aba de Transações em
componentes, hooks e utils reaproveitáveis (fix1).

Permanece, por dependerem do backend, a troca do mock pela API real (fix1) e as
regras de servidor/banco de cada issue - itens que seguem nas próprias `fix1` e
`fix2`.
