"""Utilidades compartilhadas pelos testes E2E (onboarding via API)."""

from validate_docbr import CPF, CNPJ


def registrar_e_logar(client, email="dono@empresa.com", senha="Senha@123"):
    """Cadastra um usuario pela API e devolve headers autenticados (o registro ja emite o token)."""
    payload = {
        "name": "Dono da Empresa",
        "email": email,
        "cpf": CPF().generate(),
        "password": senha,
        "birth_date": "2000-01-01",
    }
    resp = client.post("/api/register", json=payload)
    assert resp.status_code == 201, resp.get_json()
    token = resp.get_json()["token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def criar_empresa(client, headers, name="Padaria Central"):
    payload = {
        "name": name,
        "cnpj": CNPJ().generate(),
        "email": "contato@padaria.com",
        "phone": "1130000000",
    }
    resp = client.post("/api/companies", json=payload, headers=headers)
    assert resp.status_code == 201, resp.get_json()
    return resp.get_json()["company_id"]


def criar_categoria(client, headers, company_id, name="Vendas", tipo="receita"):
    resp = client.post(
        f"/api/companies/{company_id}/categories/",
        json={"name": name, "type": tipo},
        headers=headers,
    )
    assert resp.status_code == 201, resp.get_json()
    return resp.get_json()["category"]["id"]


def criar_conta_caixa(client, headers, company_id, name="Caixa Principal"):
    """Toda transacao precisa de uma conta/caixa (payment_id), entao isso e pre-requisito."""
    resp = client.post(
        f"/api/companies/{company_id}/payments/",
        json={"name": name},
        headers=headers,
    )
    assert resp.status_code == 201, resp.get_json()
    return resp.get_json()["payment"]["id"]
