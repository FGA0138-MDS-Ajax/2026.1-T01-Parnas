# Métricas de Produto

Enquanto as métricas de qualidade (GQM, M1-M4) olham para o **processo e o código**,
esta página olha para o **produto e quem o usa**. São poucos indicadores, simples,
definidos para checar se o CrediFab entrega valor: rápido, confiável e fácil de usar.

> Os valores abaixo são **metas** (o que o produto se propõe a atingir), não números de
> uso em produção. Dois deles já têm **evidência** vinda dos nossos testes (ver a última
> seção); os demais são alvos definidos para acompanhar a evolução do produto.

---
## Objetivos e indicadores

Seguindo a mesma lógica Goal-Question-Metric, mas voltada ao produto:

| Objetivo do produto                      | Pergunta                                   | Indicador                     |
|------------------------------------------|--------------------------------------------|-------------------------------|
| Ser rápido no uso                        | As telas respondem rápido?                 | **Desempenho**                |
| Ser confiável                            | Os fluxos principais funcionam sem erro?   | **Sucesso nos fluxos**        |
| Ser fácil de começar                     | O usuário chega logo ao primeiro registro? | **Tempo até o 1º lançamento** |
| Dar visão clara das finanças             | O resultado do mês fica visível?           | **Clareza financeira**        |

---
## Metas

| Indicador                | O que mede                                                        | Meta        |
|--------------------------|-------------------------------------------------------------------|-------------|
| Desempenho               | Respostas abaixo de 1s nas telas principais                       | ≥ 95%       |
| Sucesso nos fluxos       | Fluxos principais (cadastro, lançamento, conta) concluídos sem erro | ≥ 95%     |
| Tempo até o 1º lançamento| Do cadastro ao primeiro registro de transação                     | ≤ 5 min     |
| Clareza financeira       | Saldo e entradas/saídas do mês visíveis no dashboard              | 1 clique após o login |

---
## Como são obtidos

Nada de plataforma externa: os dados saem do que a aplicação **já registra**.

- **Desempenho:** percentual de respostas abaixo de 1s, medido diretamente no
  [teste de carga (Locust)](features/teste-carga-locust.md).
- **Sucesso nos fluxos:** proporção de respostas de sucesso (2xx) nas rotas dos fluxos
  principais, lida dos logs de acesso do backend; nos testes, equivale aos fluxos E2E
  passando de ponta a ponta.
- **Tempo até o 1º lançamento:** diferença entre a data de cadastro do usuário e a data
  da primeira transação dele - dois carimbos de data que o banco já guarda.
- **Clareza financeira:** verificação simples de navegação (o dashboard reúne saldo,
  entradas e saídas do mês em uma única tela, alcançável logo após o login).

---
## Evidências já coletadas

Dois indicadores não ficaram só no papel; foram medidos pelos nossos testes:

| Indicador          | Evidência                                                                 | Resultado |
|--------------------|---------------------------------------------------------------------------|-----------|
| Desempenho         | [Teste de carga (Locust)](features/teste-carga-locust.md): p95 de 20 ms   | Atingido  |
| Sucesso nos fluxos | Testes E2E de sistema (onboarding, financeiro e contas) passando          | Atingido  |

> Estas métricas complementam as de qualidade: as [métricas de qualidade](resumo-metricas.md)
> garantem que o produto é **bem construído**; as de produto garantem que ele é
> **rápido, confiável e fácil de usar**.
