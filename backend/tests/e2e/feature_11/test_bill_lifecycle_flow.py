"""E2E do ciclo de vida de conta: cria -> lista -> edita -> exclui."""

from tests.e2e.helpers import registrar_e_logar, criar_empresa, criar_categoria

DUE_DATE = "2026-12-01"


def _criar_conta(client, headers, company_id, category_id, descricao="Aluguel", valor=1500.0):
    resp = client.post(
        f"/api/companies/{company_id}/bills/",
        json={
            "description": descricao,
            "amount": valor,
            "type": "pagar",
            "due_date": DUE_DATE,
            "category_id": category_id,
        },
        headers=headers,
    )
    assert resp.status_code == 201, resp.get_json()
    return resp.get_json()["id"]


def test_ciclo_de_vida_da_conta(client, clean_db):
    headers = registrar_e_logar(client)
    company_id = criar_empresa(client, headers)
    category_id = criar_categoria(client, headers, company_id, "Despesas Fixas", "despesa")

    bill_id = _criar_conta(client, headers, company_id, category_id)

    pendentes = client.get(
        f"/api/companies/{company_id}/bills/",
        query_string={"status": "pendente"},
        headers=headers,
    )
    assert pendentes.status_code == 200
    contas = pendentes.get_json()
    assert [c["id"] for c in contas] == [bill_id]
    assert contas[0]["status"] == "pendente"

    edicao = client.put(
        f"/api/companies/{company_id}/bills/{bill_id}",
        json={"company_id": company_id, "amount": 1600.0},
        headers=headers,
    )
    assert edicao.status_code == 200

    exclusao = client.delete(
        f"/api/companies/{company_id}/bills/{bill_id}",
        query_string={"company_id": company_id},
        headers=headers,
    )
    assert exclusao.status_code == 200

    restantes = client.get(f"/api/companies/{company_id}/bills/", headers=headers)
    assert restantes.get_json() == []


def test_conta_de_empresa_alheia_nao_e_listada(client, clean_db):
    headers_a = registrar_e_logar(client, email="dono_a@empresa.com")
    company_a = criar_empresa(client, headers_a, "Empresa A")
    cat_a = criar_categoria(client, headers_a, company_a, "Despesas", "despesa")
    _criar_conta(client, headers_a, company_a, cat_a)

    headers_b = registrar_e_logar(client, email="dono_b@empresa.com")
    resp = client.get(f"/api/companies/{company_a}/bills/", headers=headers_b)
    assert resp.status_code == 403
