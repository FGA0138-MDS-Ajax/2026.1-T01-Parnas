"""Testes de QA do PR #80 - Dashboard financeiro (GET /api/dashboard).

Exercita o endpoint de dashboard de ponta a ponta (rota + service + BD em memória),
cobrindo: contrato de autenticação/validação, estrutura da resposta e o cálculo do
saldo consolidado a partir das transações reais (que são gravadas como
'receita'/'despesa' pelo TransactionService).
"""
import pytest
from datetime import date

from app.config import db
from app.models.transaction import Transaction


def _add_transaction(company_id, user_id, tipo, valor, category_id):
    t = Transaction(
        description=f"t-{tipo}-{valor}",
        amount=valor,
        date=date.today(),
        type=tipo,
        company_id=company_id,
        category_id=category_id,
        user_id=user_id,
    )
    db.session.add(t)
    db.session.commit()
    return t


class TestDashboardContrato:

    def test_dashboard_sem_token(self, client):
        # Sem JWT a rota é protegida
        resp = client.get('/api/dashboard', query_string={'company_id': 1})
        assert resp.status_code == 401

    def test_dashboard_requer_company_id(self, client, auth_headers, test_user):
        # company_id é obrigatório na query (schema)
        resp = client.get('/api/dashboard', headers=auth_headers)
        assert resp.status_code == 400
        assert 'erros_de_validacao' in resp.get_json()


class TestDashboardResposta:

    def test_estrutura_basica(self, client, auth_headers, test_company):
        resp = client.get(
            '/api/dashboard',
            query_string={'company_id': test_company.company_id},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.get_json()
        for campo in [
            'saldo_consolidado_atual',
            'mes_referencia',
            'totais_mes_atual',
            'grafico_categorias_mes',
            'contas_proximas_vencimento',
        ]:
            assert campo in data

    def test_saldo_consolidado_soma_entradas_menos_saidas(
        self, client, auth_headers, test_company, test_category, test_user
    ):
        # Transações reais são gravadas como 'receita'/'despesa'
        _add_transaction(test_company.company_id, test_user.user_id, 'receita', 300.0, test_category.category_id)
        _add_transaction(test_company.company_id, test_user.user_id, 'despesa', 100.0, test_category.category_id)

        resp = client.get(
            '/api/dashboard',
            query_string={'company_id': test_company.company_id},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.get_json()['saldo_consolidado_atual'] == 200.0
