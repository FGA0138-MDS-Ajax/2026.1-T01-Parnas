from locust import HttpUser, task, between


class SimulacaoUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        resp = self.client.post("/auth/login", json={
            "email": "carga@teste.com",
            "password": "Senha@123",
        })
        self.token = resp.json().get("token")
        self.company_id = 1

    @task
    def simular_credito(self):
        self.client.post(
            f"/api/companies/{self.company_id}/simulations/calculate",
            json={
                "requested_amount": 50000,
                "deadline_month": 24,
                "interest_rate": 1.8,
                "modality": "PRICE",
            },
            headers={"Authorization": f"Bearer {self.token}"},
            name="/simulations/calculate",
        )
