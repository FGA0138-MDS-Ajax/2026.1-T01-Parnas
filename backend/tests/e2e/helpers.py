"""
helpers.py - Utilidades compartilhadas pelos testes E2E.

Os fluxos E2E simulam um usuário real de ponta a ponta: ele se cadastra pela API,
recebe um token, cria a empresa e opera dentro dela. Estas funções encapsulam esses
primeiros passos (onboarding) para que cada teste foque no fluxo que quer validar.

CPF e CNPJ sao gerados validos em tempo de execucao (validate_docbr) para nao depender
de documentos fixos que poderiam colidir entre execucoes.
"""

from validate_docbr import CPF, CNPJ


def registrar_e_logar(client, email="dono@empresa.com", senha="Senha@123"):
    """Cadastra um usuário pela API e devolve os headers já autenticados.

    O endpoint /api/register devolve o token direto no cadastro, então o próprio
    registro já autentica o usuário (não é preciso um POST /auth/login extra).
    """
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
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def criar_empresa(client, headers, name="Padaria Central"):
    """Cria uma empresa (CNPJ válido gerado) e devolve o company_id."""
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
    """Cria uma categoria na empresa e devolve o id."""
    resp = client.post(
        f"/api/companies/{company_id}/categories/",
        json={"name": name, "type": tipo},
        headers=headers,
    )
    assert resp.status_code == 201, resp.get_json()
    return resp.get_json()["category"]["id"]


def criar_conta_caixa(client, headers, company_id, name="Caixa Principal"):
    """Cria uma conta/caixa (payment) e devolve o id.

    Toda transação precisa apontar para uma conta/caixa (payment_id é NOT NULL),
    então este passo é pré-requisito para qualquer lançamento financeiro.
    """
    resp = client.post(
        f"/api/companies/{company_id}/payments/",
        json={"name": name},
        headers=headers,
    )
    assert resp.status_code == 201, resp.get_json()
    return resp.get_json()["payment"]["id"]
