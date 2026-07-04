# Métricas de Produto

Enquanto as métricas de qualidade (GQM, M1-M4) olham para o **processo e o código**,
esta página olha para o **produto e quem o usa**: são as métricas de **negócio** e de
**experiência do usuário** que dizem se o CrediFab cumpre o seu propósito - organizar a
vida financeira de micro e pequenas empresas e prepará-las para o acesso ao crédito.

> São indicadores simples, definidos para acompanhar o valor entregue ao empreendedor.
> Os valores abaixo são as **metas do produto** e o resultado observado no **piloto**
> com contas de teste.

---
## Metas do produto

Seguindo a mesma lógica Goal-Question-Metric, mas voltada ao produto:

| Objetivo do produto                                  | Pergunta                                          | Métrica                        |
|------------------------------------------------------|---------------------------------------------------|--------------------------------|
| Organizar a vida financeira do negócio               | O usuário consegue registrar sua rotina?          | **P1 - Adoção de lançamentos** |
| Dar visão clara da saúde financeira                  | O usuário acompanha o resultado?                  | **P2 - Uso do dashboard**      |
| Preparar a empresa para o crédito                    | O usuário chega até a simulação de crédito?        | **P3 - Conversão à simulação** |
| Entregar uma experiência fluida                      | O produto é rápido e confiável no uso?            | **P4 - Desempenho percebido**  |

---
## Métricas de negócio

| Métrica                             | Definição                                                            |  Meta   | Piloto |
|-------------------------------------|---------------------------------------------------------------------|:-------:|:------:|
| P1 - Adoção de lançamentos          | Empresas que registram ao menos 1 transação na 1ª semana            |  ≥ 70%  |  78%   |
| P3 - Conversão à simulação          | Empresas que chegam à simulação de crédito após organizar as contas |  ≥ 30%  |  34%   |
| Empresas ativas por conta           | Média de empresas cadastradas por usuário                           |  ≥ 1,2  |  1,4   |
| Retenção mensal                     | Usuários que voltam ao produto no mês seguinte                      |  ≥ 40%  |  46%   |

---
## Métricas de experiência do usuário

| Métrica                             | Definição                                                       |   Meta   | Piloto |
|-------------------------------------|-----------------------------------------------------------------|:--------:|:------:|
| P2 - Uso do dashboard               | Sessões que abrem o dashboard financeiro                        |  ≥ 60%   |  67%   |
| Tempo até o 1º lançamento           | Do cadastro ao primeiro registro de transação                   | ≤ 5 min  | 3 min  |
| Tarefas concluídas sem erro         | Fluxos (cadastro, transação, conta) finalizados sem erro de uso |  ≥ 90%   |  94%   |
| P4 - Desempenho percebido           | Respostas do sistema abaixo de 1s nas telas principais          |  ≥ 95%   |  97%   |

---
## Como os dados são obtidos

A coleta é **simples e barata**: quase tudo sai de dados que a aplicação **já
guarda** no próprio banco (Postgres) ou dos **logs de acesso** do backend. Não há
plataforma de analytics externa; são consultas periódicas e contagens sobre tabelas
que já existem (`user`, `company`, `transaction`, `simulation`), todas com data de
criação registrada.

### Fonte de cada grupo de métrica

| Grupo                     | Fonte                        | Como é calculado (em linguagem simples)                                             |
|---------------------------|------------------------------|-------------------------------------------------------------------------------------|
| Métricas de negócio       | **Banco da aplicação**       | Contagens e proporções sobre `company`, `transaction` e `simulation` por período    |
| Experiência (uso/erro)    | **Logs de acesso do backend**| Cada requisição registra rota, código de resposta e tempo; agregamos por sessão     |
| Experiência (tempo/prazo) | **Banco da aplicação**       | Diferença entre carimbos de data (ex.: cadastro do usuário → 1º lançamento)          |
| Desempenho percebido      | **Logs + Locust**            | Percentual de respostas abaixo de 1s; sob carga, medido no [teste Locust](features/teste-carga-locust.md) |

### Exemplos de definição operacional

- **Adoção de lançamentos (P1):** empresas que registraram **pelo menos 1 transação
  nos 7 primeiros dias** após o cadastro, divididas pelo total de empresas criadas no
  período. Sai de uma contagem em `transaction` cruzada com a data de criação da `company`.
- **Conversão à simulação (P3):** entre as empresas que já organizaram contas/transações,
  quantas chegaram a **criar ao menos 1 simulação de crédito** (`simulation`).
- **Uso do dashboard (P2):** sessões que chamaram `GET /dashboard` sobre o total de
  sessões autenticadas, lido dos logs de acesso.
- **Tempo até o 1º lançamento:** média da diferença entre o carimbo de cadastro do
  usuário e o carimbo da primeira transação dele.
- **Tarefas concluídas sem erro:** proporção de respostas **2xx** sobre o total nas
  rotas dos fluxos principais (cadastro, transação, conta).

### O que é o "Piloto"

Os valores da coluna **Piloto** vêm de uma **rodada controlada** com contas de teste
(a própria equipe e alguns convidados) operando o produto por uma janela definida.
Durante essa janela, rodamos as consultas acima sobre o banco e os logs e registramos o
resultado. É uma amostra pequena, com finalidade de **validar as definições das
métricas** e servir de linha de base - não uma medição de produção em larga escala.

---
## Alinhamento com o propósito (ODS 9)

O CrediFab nasce alinhado ao **Objetivo de Desenvolvimento Sustentável 9** (acesso de
pequenas empresas a serviços financeiros e crédito). As métricas de produto medem
justamente esse caminho: quanto mais empresas **organizam suas finanças** (P1, P2) e
**avançam até a simulação de crédito** (P3), mais o produto cumpre sua missão de reduzir
a barreira ao crédito por falta de organização financeira.

> Estas métricas complementam as de qualidade: as [métricas de qualidade](resumo-metricas.md)
> garantem que o produto é **bem construído**; as de produto garantem que ele é
> **útil para quem usa**.
