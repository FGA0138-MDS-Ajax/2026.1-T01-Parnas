"""Testes de QA do PR #81 - Integração de Contas a pagar/receber (/api/contas).

Cobre o CRUD de contas, a quitação (que marca 'quitado' e gera transação) e o
controle de acesso por empresa. Service: BillService.
"""
import pytest
from datetime import date, timedelta

URL = "/api/contas/"


def _payload(category_id, company_id, **over):
    base = {
        "description": "Aluguel",
        "amount": 1200.0,
        "type": "pagar",
        "due_date": str(date.today() + timedelta(days=5)),
        "category_id": category_id,
        "company_id": company_id,
    }
    base.update(over)
    return base


def _cria(client, headers, test_category, **over):
    return client.post(
        URL, json=_payload(test_category.category_id, test_category.company_id, **over), headers=headers
    )


class TestContasCRUD:

    def test_cria_conta(self, client, auth_headers, test_category):
        resp = _cria(client, auth_headers, test_category)
        assert resp.status_code == 201
        assert "id" in resp.get_json()

    def test_cria_sem_token(self, client, test_category):
        resp = client.post(URL, json=_payload(test_category.category_id, test_category.company_id))
        assert resp.status_code == 401

    def test_cria_faltando_campo_obrigatorio(self, client, auth_headers, test_category):
        payload = _payload(test_category.category_id, test_category.company_id)
        del payload["amount"]
        resp = client.post(URL, json=payload, headers=auth_headers)
        assert resp.status_code == 400

    def test_lista_contas_da_empresa(self, client, auth_headers, test_category):
        _cria(client, auth_headers, test_category)
        resp = client.get(URL, query_string={"company_id": test_category.company_id}, headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.get_json()) >= 1

    def test_lista_requer_company_id(self, client, auth_headers, test_user):
        resp = client.get(URL, headers=auth_headers)
        assert resp.status_code == 400


class TestContasQuitacao:

    def test_quitar_marca_quitado(self, client, auth_headers, test_category):
        bid = _cria(client, auth_headers, test_category).get_json()["id"]
        resp = client.patch(
            f"{URL}{bid}/quitar", query_string={"company_id": test_category.company_id}, headers=auth_headers
        )
        assert resp.status_code == 200

        contas = client.get(
            URL, query_string={"company_id": test_category.company_id}, headers=auth_headers
        ).get_json()
        conta = next(c for c in contas if c["id"] == bid)
        assert conta["status"] == "quitado"

    def test_nao_edita_conta_quitada(self, client, auth_headers, test_category):
        bid = _cria(client, auth_headers, test_category).get_json()["id"]
        client.patch(
            f"{URL}{bid}/quitar", query_string={"company_id": test_category.company_id}, headers=auth_headers
        )
        resp = client.put(
            f"{URL}{bid}", json={"company_id": test_category.company_id, "description": "x"}, headers=auth_headers
        )
        assert resp.status_code == 400


class TestContasAcesso:

    def test_acesso_negado_a_empresa_sem_vinculo(self, client, auth_headers, test_user):
        resp = client.get(URL, query_string={"company_id": 9999}, headers=auth_headers)
        assert resp.status_code == 403
