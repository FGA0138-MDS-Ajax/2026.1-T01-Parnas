"""E2E da quitacao de conta: quitar gera transacao e afeta o saldo."""

from tests.e2e.helpers import registrar_e_logar, criar_empresa, criar_categoria

DUE_DATE = "2026-12-01"


def test_quitar_conta_gera_transacao_e_afeta_o_saldo(client, clean_db):
    headers = registrar_e_logar(client)
    company_id = criar_empresa(client, headers)
    category_id = criar_categoria(client, headers, company_id, "Despesas Fixas", "despesa")

    criacao = client.post(
        f"/api/companies/{company_id}/bills/",
        json={
            "description": "Fornecedor",
            "amount": 800.0,
            "type": "pagar",
            "due_date": DUE_DATE,
            "category_id": category_id,
        },
        headers=headers,
    )
    assert criacao.status_code == 201, criacao.get_json()
    bill_id = criacao.get_json()["id"]

    quitacao = client.patch(
        f"/api/companies/{company_id}/bills/{bill_id}/quitar",
        query_string={"company_id": company_id},
        headers=headers,
    )
    assert quitacao.status_code == 200, quitacao.get_json()
    assert "transaction_id" in quitacao.get_json()

    quitadas = client.get(
        f"/api/companies/{company_id}/bills/",
        query_string={"status": "quitado"},
        headers=headers,
    )
    assert [c["id"] for c in quitadas.get_json()] == [bill_id]

    historico = client.get(f"/api/companies/{company_id}/transactions/", headers=headers)
    corpo = historico.get_json()
    assert corpo["paginacao"]["total_items"] == 1
    assert corpo["resumo"]["total_despesas"] == 800.0

    dashboard = client.get(f"/api/companies/{company_id}/dashboard/", headers=headers)
    assert dashboard.get_json()["saldo_consolidado_atual"] == -800.0


def test_conta_quitada_nao_pode_ser_editada(client, clean_db):
    headers = registrar_e_logar(client)
    company_id = criar_empresa(client, headers)
    category_id = criar_categoria(client, headers, company_id, "Despesas", "despesa")

    criacao = client.post(
        f"/api/companies/{company_id}/bills/",
        json={
            "description": "Conta",
            "amount": 300.0,
            "type": "pagar",
            "due_date": DUE_DATE,
            "category_id": category_id,
        },
        headers=headers,
    )
    bill_id = criacao.get_json()["id"]

    client.patch(
        f"/api/companies/{company_id}/bills/{bill_id}/quitar",
        query_string={"company_id": company_id},
        headers=headers,
    )

    edicao = client.put(
        f"/api/companies/{company_id}/bills/{bill_id}",
        json={"company_id": company_id, "amount": 999.0},
        headers=headers,
    )
    assert edicao.status_code == 400
