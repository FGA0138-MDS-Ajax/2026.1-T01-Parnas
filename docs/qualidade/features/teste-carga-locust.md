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
| Tempo de resposta no percentil 95 (p95)    | **< 1000 ms**     | P4 - Desempenho percebido        |
| Taxa de erro (respostas não-2xx)           | **< 1%**          | Estabilidade sob carga           |
| Usuários simultâneos sustentados           | **50 usuários**   | Carga esperada de pico do piloto |

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

Execução headless, 50 usuários, 2 minutos, endpoint `/simulations/calculate`:

| Métrica                         | Valor       | SLO       | Situação |
|---------------------------------|:-----------:|:---------:|:--------:|
| Requisições totais              | 3.184       | -         | -        |
| Falhas                          | 0 (0,00%)   | < 1%      | OK       |
| Vazão (RPS)                     | ~27 req/s   | -         | -        |
| Tempo mediano (p50)             | 85 ms       | -         | -        |
| Percentil 95 (p95)              | 240 ms      | < 1000 ms | OK       |
| Percentil 99 (p99)              | 410 ms      | -         | -        |
| Tempo máximo                    | 890 ms      | < 1000 ms | OK       |

---
## 6. Análise

- **Sem falhas:** as 3.184 requisições retornaram 2xx (0% de erro), abaixo do limite de 1%.
- **Dentro do prazo:** o p95 (240 ms) ficou bem abaixo do teto de 1s, e mesmo o pior
  caso (890 ms) não estourou o limite - ou seja, **97% das respostas abaixo de 1s**,
  o que sustenta a métrica de produto **P4 (desempenho percebido)**.
- **Vazão estável:** ~27 req/s sustentados com 50 usuários simultâneos, sem degradação
  crescente ao longo dos 2 minutos (sem sinal de vazamento de recursos/fila crescente).

---
## 7. Parecer final

> **Status:** Aprovada
>
> O sistema atendeu a todos os critérios de desempenho (SLO) no endpoint mais custoso:
> zero falhas, p95 de 240 ms (limite de 1s) e vazão estável de ~27 req/s com 50 usuários
> simultâneos. O requisito não funcional **R14 (Desempenho)** está satisfeito para a carga
> esperada. Recomenda-se repetir o teste caso o volume de usuários projetado cresça de
> forma relevante.
