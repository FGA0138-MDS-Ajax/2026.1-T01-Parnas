URL = "/api/simulations/"
CALC = "/api/simulations/calculate"


def _payload(company_id=None, **over):
    base = {
        "requested_amount": 12000.0,
        "deadline_month": 12,
        "interest_rate": 2.0,
        "modality": "PRICE",
    }
    if company_id is not None:
        base["company_id"] = company_id
    base.update(over)
    return base


def test_calcular_price_retorna_detalhamento_sem_persistir(client, auth_headers, test_company):
    resp = client.post(CALC, json=_payload(), headers=auth_headers)

    assert resp.status_code == 200
    body = resp.get_json()
    assert body["resumo"]["modalidade"] == "PRICE"
    assert len(body["detalhamento_mensal"]) == 12

    lista = client.get(f"{URL}?company_id={test_company.company_id}", headers=auth_headers)
    assert lista.get_json()["simulations"] == []


def test_calcular_modalidade_invalida_retorna_400(client, auth_headers):
    resp = client.post(CALC, json=_payload(modality="XPTO"), headers=auth_headers)

    assert resp.status_code == 400


def test_calcular_valor_negativo_retorna_400(client, auth_headers):
    resp = client.post(CALC, json=_payload(requested_amount=-5.0), headers=auth_headers)

    assert resp.status_code == 400


def test_calcular_sem_token_retorna_401(client):
    resp = client.post(CALC, json=_payload())

    assert resp.status_code == 401


def test_salvar_simulacao_retorna_id(client, auth_headers, test_company):
    resp = client.post(URL, json=_payload(company_id=test_company.company_id), headers=auth_headers)

    assert resp.status_code == 201
    assert "simulation_id" in resp.get_json()


def test_salvar_sem_company_id_retorna_400(client, auth_headers):
    resp = client.post(URL, json=_payload(), headers=auth_headers)

    assert resp.status_code == 400


def test_listar_traz_apenas_simulacoes_da_empresa(client, auth_headers, test_company):
    client.post(URL, json=_payload(company_id=test_company.company_id), headers=auth_headers)
    client.post(URL, json=_payload(company_id=test_company.company_id, modality="SAC"), headers=auth_headers)

    resp = client.get(f"{URL}?company_id={test_company.company_id}", headers=auth_headers)

    assert resp.status_code == 200
    assert len(resp.get_json()["simulations"]) == 2


def test_listar_sem_company_id_retorna_400(client, auth_headers):
    resp = client.get(URL, headers=auth_headers)

    assert resp.status_code == 400


def test_excluir_simulacao_existente_some_da_listagem(client, auth_headers, test_company):
    criada = client.post(URL, json=_payload(company_id=test_company.company_id), headers=auth_headers)
    sim_id = criada.get_json()["simulation_id"]

    resp = client.delete(f"{URL}{sim_id}?company_id={test_company.company_id}", headers=auth_headers)

    assert resp.status_code == 200
    lista = client.get(f"{URL}?company_id={test_company.company_id}", headers=auth_headers)
    assert lista.get_json()["simulations"] == []


def test_excluir_simulacao_inexistente_retorna_404(client, auth_headers, test_company):
    resp = client.delete(f"{URL}9999?company_id={test_company.company_id}", headers=auth_headers)

    assert resp.status_code == 404
