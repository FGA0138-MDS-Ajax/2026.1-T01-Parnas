"""
test_finance_flow.py - E2E do fluxo financeiro (transações + dashboard).

Percorre a jornada completa de um usuário que acabou de entrar no sistema:
cadastro -> empresa -> categorias -> lançamento de receita e despesa ->
consulta do histórico -> visão consolidada no dashboard.

O foco é validar que os dados "atravessam" a aplicação: o que foi lançado via
POST reaparece no histórico e é somado corretamente no saldo do dashboard.
"""

from tests.e2e.helpers import (
    registrar_e_logar, criar_empresa, criar_categoria, criar_conta_caixa,
)

# data claramente no passado: o schema de transação barra datas futuras.
DATA_LANCAMENTO = "2026-01-10"


def _lancar_transacao(client, headers, company_id, category_id, payment_id, descricao, valor, tipo):
    resp = client.post(
        f"/api/companies/{company_id}/transactions/",
        json={
            "description": descricao,
            "amount": valor,
            "date": DATA_LANCAMENTO,
            "type": tipo,
            "category_id": category_id,
            "payment_id": payment_id,
        },
        headers=headers,
    )
    assert resp.status_code == 201, resp.get_json()
    return resp.get_json()["transaction_id"]


def test_lancamentos_aparecem_no_historico_e_somam_no_dashboard(client, clean_db):
    headers = registrar_e_logar(client)
    company_id = criar_empresa(client, headers)
    cat_receita = criar_categoria(client, headers, company_id, "Vendas", "receita")
    cat_despesa = criar_categoria(client, headers, company_id, "Fornecedores", "despesa")
    caixa = criar_conta_caixa(client, headers, company_id)

    # Lança uma receita de 1000 e uma despesa de 400.
    _lancar_transacao(client, headers, company_id, cat_receita, caixa, "Venda do dia", 1000.0, "receita")
    _lancar_transacao(client, headers, company_id, cat_despesa, caixa, "Compra de insumos", 400.0, "despesa")

    # Histórico traz as duas e fecha o resumo (1000 - 400 = 600).
    historico = client.get(f"/api/companies/{company_id}/transactions/", headers=headers)
    assert historico.status_code == 200
    corpo = historico.get_json()
    assert corpo["paginacao"]["total_items"] == 2
    assert corpo["resumo"]["total_receitas"] == 1000.0
    assert corpo["resumo"]["total_despesas"] == 400.0
    assert corpo["resumo"]["saldo"] == 600.0

    # Dashboard consolida o mesmo saldo.
    dashboard = client.get(f"/api/companies/{company_id}/dashboard/", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.get_json()["saldo_consolidado_atual"] == 600.0


def test_transacao_em_empresa_de_outro_usuario_e_barrada(client, clean_db):
    # Usuário A monta empresa e categoria.
    headers_a = registrar_e_logar(client, email="a@empresa.com")
    company_a = criar_empresa(client, headers_a, "Empresa A")
    cat_a = criar_categoria(client, headers_a, company_a)

    # Usuário B, sem vínculo com a empresa A, tenta lançar transação nela.
    headers_b = registrar_e_logar(client, email="b@empresa.com")
    resp = client.post(
        f"/api/companies/{company_a}/transactions/",
        json={
            "description": "Invasao",
            "amount": 100.0,
            "date": DATA_LANCAMENTO,
            "type": "receita",
            "category_id": cat_a,
        },
        headers=headers_b,
    )

    # Acesso negado e nada persiste para o usuário B.
    assert resp.status_code == 403
    historico_a = client.get(f"/api/companies/{company_a}/transactions/", headers=headers_a)
    assert historico_a.get_json()["paginacao"]["total_items"] == 0
