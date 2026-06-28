import pytest

from app.config import db

URL = "/api/comparacoes/"
CALC = "/api/comparacoes/calcular"


@pytest.fixture
def ctx(test_user, test_company):
    """O ComparisonService usa user.company_id; o conftest vincula via M2M, então
    setamos o FK direto aqui."""
    test_user.company_id = test_company.company_id
    db.session.commit()
    return {"company_id": test_company.company_id, "user_id": test_user.user_id}


def _payload(**over):
    base = {
        "loan_amount": 10000,
        "modalities": [
            {"name": "Banco A", "interest_rate": 2.0, "term_months": 12, "type": "PJ"},
            {"name": "Financeira B", "interest_rate": 5.0, "term_months": 12, "type": "PF"},
        ],
    }
    base.update(over)
    return base


def test_calcular_retorna_comparacao_melhor_opcao_e_alerta_pf(client, auth_headers, ctx):
    resp = client.post(CALC, json=_payload(), headers=auth_headers)

    assert resp.status_code == 200
    body = resp.get_json()
    assert len(body["comparisons"]) == 2
    assert sum(1 for c in body["comparisons"] if c["is_best_option"]) == 1
    pf = next(c for c in body["comparisons"] if c["type"] == "PF")
    assert pf["warning_pf"] is True


def test_calcular_acima_de_4_modalidades_retorna_400(client, auth_headers, ctx):
    modalidades = [{"name": f"M{i}", "interest_rate": 2, "term_months": 12, "type": "PJ"} for i in range(5)]
    resp = client.post(CALC, json=_payload(modalities=modalidades), headers=auth_headers)

    assert resp.status_code == 400


def test_calcular_sem_token_retorna_401(client, ctx):
    resp = client.post(CALC, json=_payload())

    assert resp.status_code == 401


def test_salvar_comparacao_retorna_id(client, auth_headers, ctx):
    resp = client.post(URL, json=_payload(), headers=auth_headers)

    assert resp.status_code == 201
    assert "id" in resp.get_json()


def test_listar_comparacoes_da_empresa(client, auth_headers, ctx):
    client.post(URL, json=_payload(), headers=auth_headers)

    resp = client.get(URL, headers=auth_headers)

    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_excluir_comparacao_existente(client, auth_headers, ctx):
    criada = client.post(URL, json=_payload(), headers=auth_headers).get_json()

    resp = client.delete(f"{URL}{criada['id']}", headers=auth_headers)

    assert resp.status_code == 200
    assert client.get(URL, headers=auth_headers).get_json() == []


def test_excluir_comparacao_inexistente_retorna_404(client, auth_headers, ctx):
    resp = client.delete(f"{URL}9999", headers=auth_headers)

    assert resp.status_code == 404


def test_exportar_pdf_de_comparacao_existente(client, auth_headers, ctx):
    criada = client.post(URL, json=_payload(), headers=auth_headers).get_json()

    resp = client.get(f"{URL}{criada['id']}/exportar", headers=auth_headers)

    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"


def test_exportar_pdf_inexistente_retorna_404(client, auth_headers, ctx):
    resp = client.get(f"{URL}9999/exportar", headers=auth_headers)

    assert resp.status_code == 404
