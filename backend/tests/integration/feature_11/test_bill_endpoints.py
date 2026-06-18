import pytest
from datetime import date

from app.config import db
from app.models.bill import Bill

URL = "/api/contas/"


@pytest.fixture
def contexto(test_user, test_company, test_category):
    """Liga o usuário autenticado à empresa (o BillService usa user.company_id)
    e disponibiliza uma categoria válida da mesma empresa."""
    test_user.company_id = test_company.company_id
    db.session.commit()
    return {"company_id": test_company.company_id, "category_id": test_category.category_id}


def _payload(category_id, **over):
    base = {
        "description": "Aluguel",
        "amount": 1000.0,
        "type": "pagar",
        "due_date": "2026-07-01",
        "category_id": category_id,
    }
    base.update(over)
    return base


def _cria_bill_direto(contexto, **over):
    """Insere uma conta direto no banco (para montar estados como 'quitado')."""
    base = dict(
        description="Conta", amount=500, type="pagar",
        due_date=date(2026, 7, 1), category_id=contexto["category_id"],
        company_id=contexto["company_id"],
    )
    base.update(over)
    bill = Bill(**base)
    db.session.add(bill)
    db.session.commit()
    return bill


def test_cria_conta_dados_validos(client, auth_headers, contexto):
    resp = client.post(URL, json=_payload(contexto["category_id"]), headers=auth_headers)

    assert resp.status_code == 201
    assert "id" in resp.get_json()


def test_cria_conta_campos_faltando_retorna_400(client, auth_headers, contexto):
    payload = _payload(contexto["category_id"])
    payload.pop("amount")

    resp = client.post(URL, json=payload, headers=auth_headers)

    assert resp.status_code == 400


def test_cria_conta_sem_token_retorna_401(client, contexto):
    resp = client.post(URL, json=_payload(contexto["category_id"]))

    assert resp.status_code == 401


def test_lista_contas_da_empresa(client, auth_headers, contexto):
    client.post(URL, json=_payload(contexto["category_id"]), headers=auth_headers)
    client.post(URL, json=_payload(contexto["category_id"], description="Internet"), headers=auth_headers)

    resp = client.get(URL, headers=auth_headers)

    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_lista_filtra_por_status(client, auth_headers, contexto):
    client.post(URL, json=_payload(contexto["category_id"]), headers=auth_headers)
    _cria_bill_direto(contexto, status="quitado", description="Paga")

    pendentes = client.get(f"{URL}?status=pendente", headers=auth_headers).get_json()
    quitadas = client.get(f"{URL}?status=quitado", headers=auth_headers).get_json()

    assert [c["description"] for c in pendentes] == ["Aluguel"]
    assert [c["description"] for c in quitadas] == ["Paga"]


def test_edita_conta_pendente(client, auth_headers, contexto):
    bill = _cria_bill_direto(contexto, description="Antigo")

    resp = client.put(f"{URL}{bill.bill_id}", json={"description": "Novo"}, headers=auth_headers)

    assert resp.status_code == 200


def test_edita_conta_inexistente_retorna_404(client, auth_headers, contexto):
    resp = client.put(f"{URL}9999", json={"description": "x"}, headers=auth_headers)

    assert resp.status_code == 404


def test_exclui_conta_pendente(client, auth_headers, contexto):
    bill = _cria_bill_direto(contexto)

    resp = client.delete(f"{URL}{bill.bill_id}", headers=auth_headers)

    assert resp.status_code == 200
    assert client.get(URL, headers=auth_headers).get_json() == []


def test_exclui_conta_inexistente_retorna_404(client, auth_headers, contexto):
    resp = client.delete(f"{URL}9999", headers=auth_headers)

    assert resp.status_code == 404


def test_conta_quitada_nao_pode_ser_editada(client, auth_headers, contexto):
    bill = _cria_bill_direto(contexto, status="quitado")

    resp = client.put(f"{URL}{bill.bill_id}", json={"description": "x"}, headers=auth_headers)

    assert resp.status_code == 400


def test_conta_quitada_nao_pode_ser_excluida(client, auth_headers, contexto):
    bill = _cria_bill_direto(contexto, status="quitado")

    resp = client.delete(f"{URL}{bill.bill_id}", headers=auth_headers)

    assert resp.status_code == 400


def test_quitar_conta_ja_quitada_retorna_400(client, auth_headers, contexto):
    bill = _cria_bill_direto(contexto, status="quitado")

    resp = client.patch(f"{URL}{bill.bill_id}/quitar", headers=auth_headers)

    assert resp.status_code == 400


@pytest.mark.xfail(
    reason="DEF-01: BillService.pay_bill cria Transaction sem 'type', mas "
           "Transaction.type é NOT NULL → IntegrityError ao quitar.",
    strict=False,
)
def test_quitar_conta_pendente_gera_transacao(client, auth_headers, contexto):
    bill = _cria_bill_direto(contexto, status="pendente")

    resp = client.patch(f"{URL}{bill.bill_id}/quitar", headers=auth_headers)

    assert resp.status_code == 200
    assert "transação" in resp.get_json().get("mensagem", "").lower()
