import pytest
from datetime import date

from app.config import db
from app.models.company import Company
from app.models.transaction import Transaction

URL = "/api/reports"
CNPJ_FORMATADO = "11.222.333/0001-81"
CNPJ_DIGITOS = "11222333000181"


@pytest.fixture
def ctx(test_user, test_company, test_category):
    """A empresa de produção guarda o CNPJ só com dígitos (company_service limpa);
    o conftest cria formatado, então normalizamos aqui. O test_user já está
    vinculado à empresa (user_company) pelo fixture test_company."""
    test_company.cnpj = CNPJ_DIGITOS
    db.session.commit()
    return {
        "cnpj": CNPJ_FORMATADO,
        "company_id": test_company.company_id,
        "category_id": test_category.category_id,
        "user_id": test_user.user_id,
    }


def _q(ctx, **over):
    base = {"cnpj": ctx["cnpj"], "period": "mensal", "month": 6, "year": 2026}
    base.update(over)
    return base


def _tx(ctx, tipo, valor, dia):
    t = Transaction(
        type=tipo, description="x", amount=valor, date=date(2026, 6, dia),
        company_id=ctx["company_id"], user_id=ctx["user_id"], category_id=ctx["category_id"],
    )
    db.session.add(t)
    db.session.commit()


def test_relatorio_sem_token_retorna_401(client, ctx):
    resp = client.get(URL, query_string=_q(ctx))

    assert resp.status_code == 401


def test_relatorio_sem_cnpj_retorna_400(client, auth_headers, ctx):
    resp = client.get(URL, query_string={"period": "anual", "year": 2026}, headers=auth_headers)

    assert resp.status_code == 400


def test_relatorio_period_invalido_retorna_400(client, auth_headers, ctx):
    resp = client.get(URL, query_string=_q(ctx, period="trimestral"), headers=auth_headers)

    assert resp.status_code == 400


def test_relatorio_empresa_inexistente_retorna_404(client, auth_headers, ctx):
    resp = client.get(URL, query_string=_q(ctx, cnpj="00000000000000"), headers=auth_headers)

    assert resp.status_code == 404


def test_relatorio_usuario_sem_acesso_retorna_403(client, auth_headers, ctx):
    outra = Company(name="Outra", cnpj="99888777000166", email="o@e.com", phone="1130000000")
    db.session.add(outra)
    db.session.commit()

    resp = client.get(URL, query_string=_q(ctx, cnpj="99.888.777/0001-66"), headers=auth_headers)

    assert resp.status_code == 403


def test_relatorio_mensal_sem_mes_e_ano_retorna_400(client, auth_headers, ctx):
    resp = client.get(URL, query_string={"cnpj": ctx["cnpj"], "period": "mensal"}, headers=auth_headers)

    assert resp.status_code == 400


def test_relatorio_periodo_invertido_retorna_400(client, auth_headers, ctx):
    resp = client.get(
        URL,
        query_string={"cnpj": ctx["cnpj"], "start_date": "2026-06-10", "end_date": "2026-06-01"},
        headers=auth_headers,
    )

    assert resp.status_code == 400


def test_relatorio_mensal_retorna_estrutura_e_periodo(client, auth_headers, ctx):
    resp = client.get(URL, query_string=_q(ctx), headers=auth_headers)

    assert resp.status_code == 200
    body = resp.get_json()
    assert {"periodo", "totais", "distribuicao_categorias", "evolucao"}.issubset(body)
    assert body["periodo"]["data_inicio"] == "2026-06-01"
    assert body["periodo"]["data_fim"] == "2026-06-30"


def test_relatorio_periodo_personalizado_retorna_200(client, auth_headers, ctx):
    resp = client.get(
        URL,
        query_string={"cnpj": ctx["cnpj"], "start_date": "2026-03-01", "end_date": "2026-03-31"},
        headers=auth_headers,
    )

    assert resp.status_code == 200
    assert resp.get_json()["periodo"]["data_inicio"] == "2026-03-01"


@pytest.mark.xfail(
    reason="DEF-02: report_service filtra Transaction.type == 'ENTRADA'/'SAIDA', "
           "mas as transações usam 'receita'/'despesa' → totais sempre zerados.",
    strict=False,
)
def test_totais_refletem_as_transacoes_do_periodo(client, auth_headers, ctx):
    _tx(ctx, "receita", 1000.0, 5)
    _tx(ctx, "despesa", 400.0, 6)

    resp = client.get(URL, query_string=_q(ctx), headers=auth_headers)

    totais = resp.get_json()["totais"]
    assert totais["total_receitas"] == 1000.0
    assert totais["total_despesas"] == 400.0
    assert totais["saldo"] == 600.0
