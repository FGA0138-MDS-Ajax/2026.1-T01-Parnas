# Documentação de Testes - Teste de Carga (Locust)

Relatório do **teste de carga** do CrediFab, correspondente ao caso **TS-27** do
[Roteiro de Testes](../roteiro-testes.md). Diferente dos demais relatórios (que testam
uma feature funcional), este mede um requisito **não funcional**: o desempenho do
sistema sob **muitos acessos simultâneos**.

---
## 1. Identificação

| Campo                | Valor                                                        |
|----------------------|--------------------------------------------------------------|
| **Alvo**             | Endpoint de simulação de crédito (`POST .../simulations/calculate`) |
| **Cenário**          | CEN-04                                                       |
| **Requisito**        | R14 - Desempenho                                             |
| **Caso de teste**    | TS-27 (Carga)                                                |
| **Ferramenta**       | Locust                                                       |
| **Sprint**           | 10                                                           |
| **Responsáveis**     | Daniel Filipe / Matheus Moretti                             |
| **Data**             | 04/07/2026                                                   |

> O endpoint de simulação foi escolhido por ser o **mais pesado em CPU** do sistema
> (cálculo de Tabela Price/SAC e projeção de fluxo), sendo o candidato natural a gargalo.

---
## 2. Objetivo e critérios de aceitação (SLO)

O teste verifica se o sistema **aguenta a carga esperada** mantendo tempos de resposta
e taxa de erro dentro dos limites acordados (SLO - *Service Level Objective*):

| Critério                                   | Limite            | Ligado a                         |
|--------------------------------------------|-------------------|----------------------------------|
| Tempo de resposta no percentil 95 (p95)    | **< 1000 ms**     | Desempenho (métricas de produto) |
| Taxa de erro (respostas não-2xx)           | **< 1%**          | Estabilidade sob carga           |
| Usuários simultâneos sustentados           | **50 usuários**   | Carga esperada de pico          |

---
## 3. Cenário de carga

| Parâmetro              | Valor                                       |
|------------------------|---------------------------------------------|
| Usuários virtuais      | 50                                          |
| Ramp-up (spawn rate)   | 5 usuários/segundo                          |
| Duração                | 2 minutos                                   |
| Comportamento          | Login uma vez, depois simulações repetidas  |
| Intervalo entre ações  | 1 a 3 segundos por usuário                  |

Cada usuário virtual **autentica uma vez** (guardando o token JWT) e passa a disparar
requisições de simulação, imitando um empreendedor testando cenários de crédito.

---
## 4. Como executar

### 4.1. Instalar o Locust

```bash
pip install locust
```

### 4.2. Subir o backend alvo

```bash
cd backend
flask run          # ou: python run.py  (host padrao http://localhost:5000)
```

> Deixe pré-cadastrada uma conta de teste (`carga@teste.com` / `Senha@123`) com uma
> empresa (`company_id = 1`), para o script conseguir autenticar e simular.

### 4.3. Criar o arquivo `locustfile.py`

```python
from locust import HttpUser, task, between


class SimulacaoUser(HttpUser):
    # cada usuario espera de 1 a 3s entre uma acao e outra
    wait_time = between(1, 3)

    def on_start(self):
        # roda uma vez quando o usuario virtual "entra": faz login e guarda o token
        resp = self.client.post("/auth/login", json={
            "email": "carga@teste.com",
            "password": "Senha@123",
        })
        self.token = resp.json().get("token")
        self.company_id = 1  # empresa de teste pre-criada

    @task
    def simular_credito(self):
        self.client.post(
            f"/api/companies/{self.company_id}/simulations/calculate",
            json={
                "requested_amount": 50000,   # valor solicitado
                "deadline_month": 24,        # prazo em meses
                "interest_rate": 1.8,        # taxa de juros (% ao mes)
                "modality": "PRICE",         # sistema de amortizacao (PRICE/SAC)
            },
            headers={"Authorization": f"Bearer {self.token}"},
            name="/simulations/calculate",   # agrupa as metricas sob um nome fixo
        )
```

> Ajuste os nomes dos campos do JSON ao schema real de cálculo do backend
> (`requested_amount`, `deadline_month`, `interest_rate`, `modality`) se ele mudar.

### 4.4. Rodar o teste

**Com interface web** (recomendado para explorar):

```bash
locust -f locustfile.py --host http://localhost:5000
# abra http://localhost:8089 e informe: 50 usuarios, spawn rate 5
```

**Sem interface (headless), já com os parâmetros do cenário:**

```bash
locust -f locustfile.py --host http://localhost:5000 \
       --users 50 --spawn-rate 5 --run-time 2m --headless
```

O Locust imprime, ao vivo e no fim, a tabela de estatísticas (requisições, falhas,
p50/p95/p99 e RPS). Para gerar um relatório HTML, acrescente `--html relatorio.html`.

---
## 5. Resultados

Execução real, headless, 50 usuários, 2 minutos. Ambiente: servidor Flask (modo
`threaded`) + SQLite local. O endpoint sob teste é o `/simulations/calculate`; o
`/auth/login` aparece à parte porque roda **uma vez por usuário** (custo de `bcrypt`),
não é o alvo da carga.

**Endpoint `/simulations/calculate` (alvo):**

| Métrica                         | Valor       | SLO       | Situação |
|---------------------------------|:-----------:|:---------:|:--------:|
| Requisições                     | 2.848       | -         | -        |
| Falhas                          | 0 (0,00%)   | < 1%      | OK       |
| Vazão                           | ~24 req/s   | -         | -        |
| Tempo mediano (p50)             | 12 ms       | -         | -        |
| Percentil 95 (p95)              | 20 ms       | < 1000 ms | OK       |
| Percentil 99 (p99)              | 27 ms       | -         | -        |
| Tempo máximo                    | 39 ms       | < 1000 ms | OK       |

**Totais da execução:** 2.898 requisições (50 login + 2.848 simulações), **0 falhas**.
O `/auth/login` teve média de ~558 ms (esperado: o `bcrypt` é propositalmente custoso),
mas ocorre só na entrada de cada usuário.

---
## 6. Análise

- **Sem falhas:** as 2.898 requisições retornaram 2xx (0% de erro), bem abaixo do limite de 1%.
- **Muito dentro do prazo:** o p95 do endpoint alvo (20 ms) ficou a duas ordens de
  grandeza do teto de 1s, e mesmo o pior caso (39 ms) não chegou perto - **100% das
  simulações abaixo de 1s**, sustentando com folga a métrica de produto de **desempenho**.
- **Vazão estável:** ~24 req/s sustentados com 50 usuários simultâneos ao longo dos 2
  minutos, sem degradação crescente (sem sinal de fila crescente ou vazamento de recursos).
- O cálculo de Price/SAC é leve em CPU; o único ponto caro do fluxo é o `bcrypt` do login,
  que por ser único por sessão não afeta a experiência de simular repetidas vezes.

---
## 7. Parecer final

> **Status:** Aprovada
>
> O sistema atendeu com folga a todos os critérios de desempenho (SLO) no endpoint mais
> custoso: zero falhas, p95 de 20 ms (limite de 1s) e vazão estável de ~24 req/s com 50
> usuários simultâneos. O requisito não funcional **R14 (Desempenho)** está satisfeito
> para a carga esperada. Como o teste rodou contra o servidor de desenvolvimento com
> SQLite, recomenda-se repeti-lo contra o ambiente de produção (WSGI + Postgres) caso o
> volume de usuários projetado cresça de forma relevante.
