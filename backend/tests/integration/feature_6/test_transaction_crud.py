import pytest
from datetime import date, timedelta

from app.config import db
from app.models.company import Company
from app.models.category import Category

URL = "/api/transactions/"


def _payload(category_id, company_id, **over):
    base = {
        "description": "Venda de produtos",
        "amount": 150.0,
        "date": str(date(2025, 5, 1)),
        "type": "receita",
        "category_id": category_id,
        "company_id": company_id,
    }
    base.update(over)
    return base


@pytest.fixture
def empresa_b_categoria(test_company):
    company_b = Company(name="Mercado B", cnpj="11.444.777/0001-61",
                        email="b@empresa.com", phone="1140000000")
    db.session.add(company_b)
    db.session.commit()
    cat_b = Category(name="Servicos B", type="receita", company_id=company_b.company_id)
    db.session.add(cat_b)
    db.session.commit()
    return {"company_id": company_b.company_id, "category_id": cat_b.category_id}


def _cria(client, headers, test_category, **over):
    payload = _payload(test_category.category_id, test_category.company_id, **over)
    return client.post(URL, json=payload, headers=headers)


def test_cria_transacao_dados_validos(client, auth_headers, test_category):
    # Act
    resp = _cria(client, auth_headers, test_category)

    assert resp.status_code == 201
    assert "transaction_id" in resp.get_json()


def test_cria_transacao_sem_token(client, test_category):
    # Act: sem header de autenticação
    resp = client.post(URL, json=_payload(test_category.category_id, test_category.company_id))

    assert resp.status_code == 401


def test_cria_transacao_valor_negativo(client, auth_headers, test_category):
    # Act
    resp = _cria(client, auth_headers, test_category, amount=-10.0)

    assert resp.status_code == 400
    assert "erros_de_validacao" in resp.get_json()


def test_cria_transacao_valor_zero(client, auth_headers, test_category):
    # Act: valor precisa ser positivo
    resp = _cria(client, auth_headers, test_category, amount=0)

    assert resp.status_code == 400
    assert "erros_de_validacao" in resp.get_json()


def test_cria_transacao_data_futura(client, auth_headers, test_category):
    futura = str(date.today() + timedelta(days=1))

    # Act
    resp = _cria(client, auth_headers, test_category, date=futura)

    assert resp.status_code == 400
    assert "erros_de_validacao" in resp.get_json()


def test_cria_transacao_sem_categoria(client, auth_headers, test_category):
    payload = _payload(test_category.category_id, test_category.company_id)
    del payload["category_id"]

    # Act: categoria é obrigatória
    resp = client.post(URL, json=payload, headers=auth_headers)

    assert resp.status_code == 400
    assert "erros_de_validacao" in resp.get_json()


def test_cria_transacao_categoria_de_outra_empresa(client, auth_headers, test_company, empresa_b_categoria):
    # Act: usa a categoria da empresa B, mas informa a empresa A
    resp = client.post(
        URL,
        json=_payload(empresa_b_categoria["category_id"], test_company.company_id),
        headers=auth_headers,
    )

    # Assert: categoria não pertence à empresa informada
    assert resp.status_code == 400
    assert "erro" in resp.get_json()


@pytest.mark.xfail(
    reason="DEF (herdado da feature 7): get_history_filtered quebra com TypeError 'Decimal - float' "
    "quando o histórico tem só um tipo de transação; impede confirmar 'aparece imediatamente no "
    "histórico' logo após o primeiro cadastro",
    strict=False,
)
def test_transacao_aparece_no_historico(client, auth_headers, test_category):
    _cria(client, auth_headers, test_category, description="Aluguel recebido")

    # Act: consulta o histórico da empresa
    resp = client.get(URL, query_string={"company_id": test_category.company_id}, headers=auth_headers)

    assert resp.status_code == 200
    descricoes = [t["description"] for t in resp.get_json()["transacoes"]]
    assert "Aluguel recebido" in descricoes


def test_edita_transacao_existente(client, auth_headers, test_category, app_context):
    # Arrange
    tid = _cria(client, auth_headers, test_category).get_json()["transaction_id"]

    # Act
    resp = client.put(
        f"{URL}{tid}",
        json={"company_id": test_category.company_id, "description": "Venda revisada", "amount": 250.0},
        headers=auth_headers,
    )

    # Assert: relê do banco (o GET de histórico tem bug pré-existente da feature 7)
    assert resp.status_code == 200
    from app.models.transaction import Transaction
    atualizada = db.session.get(Transaction, tid)
    assert atualizada.description == "Venda revisada"
    assert float(atualizada.amount) == 250.0


def test_edita_transacao_inexistente(client, auth_headers, test_company):
    # Act
    resp = client.put(
        f"{URL}9999",
        json={"company_id": test_company.company_id, "description": "x"},
        headers=auth_headers,
    )

    assert resp.status_code == 404


def test_edita_transacao_sem_company_id(client, auth_headers, test_category):
    tid = _cria(client, auth_headers, test_category).get_json()["transaction_id"]

    # Act: company_id é obrigatório no corpo
    resp = client.put(f"{URL}{tid}", json={"description": "x"}, headers=auth_headers)

    assert resp.status_code == 400


def test_exclui_transacao(client, auth_headers, test_category):
    tid = _cria(client, auth_headers, test_category).get_json()["transaction_id"]

    # Act
    resp = client.delete(f"{URL}{tid}", query_string={"company_id": test_category.company_id}, headers=auth_headers)

    assert resp.status_code == 200
    hist = client.get(URL, query_string={"company_id": test_category.company_id}, headers=auth_headers).get_json()
    assert hist["paginacao"]["total_items"] == 0


def test_exclui_transacao_inexistente(client, auth_headers, test_company):
    # Act
    resp = client.delete(f"{URL}9999", query_string={"company_id": test_company.company_id}, headers=auth_headers)

    assert resp.status_code == 404


def test_exclui_transacao_sem_company_id(client, auth_headers, test_category):
    tid = _cria(client, auth_headers, test_category).get_json()["transaction_id"]

    # Act: company_id é obrigatório na URL
    resp = client.delete(f"{URL}{tid}", headers=auth_headers)

    assert resp.status_code == 400


@pytest.mark.xfail(
    reason="DEF: create_transaction valida categoria↔empresa, mas não checa se o user autenticado "
    "pertence à empresa; usuário sem vínculo cria transação em empresa alheia (deveria 403)",
    strict=False,
)
def test_usuario_sem_vinculo_cria_transacao_em_empresa_alheia(client, auth_headers, test_company, empresa_b_categoria):
    # Act: test_user não está vinculado à empresa B, mas registra transação nela
    resp = client.post(
        URL,
        json=_payload(empresa_b_categoria["category_id"], empresa_b_categoria["company_id"]),
        headers=auth_headers,
    )

    # Assert: deveria ser negado por falta de vínculo do usuário com a empresa
    assert resp.status_code == 403
