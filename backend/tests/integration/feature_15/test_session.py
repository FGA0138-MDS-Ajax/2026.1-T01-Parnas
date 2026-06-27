"""Testes de QA do PR #76 - Seleção de empresa ativa.

Cobre os dois endpoints novos da sessão:
- GET  /api/usuarios/me/empresas   (lista as empresas do usuário logado)
- POST /api/sessao/empresa-ativa   (define a empresa ativa e devolve novo JWT)
"""
import pytest


class TestMinhasEmpresas:

    def test_sem_token(self, client):
        resp = client.get('/api/usuarios/me/empresas')
        assert resp.status_code == 401

    def test_lista_empresas_do_usuario(self, client, auth_headers, test_company):
        resp = client.get('/api/usuarios/me/empresas', headers=auth_headers)
        assert resp.status_code == 200
        empresas = resp.get_json()
        assert any(c['company_id'] == test_company.company_id for c in empresas)


class TestEmpresaAtiva:

    def test_sem_company_id(self, client, auth_headers, test_user):
        resp = client.post('/api/sessao/empresa-ativa', json={}, headers=auth_headers)
        assert resp.status_code == 400

    def test_empresa_que_nao_pertence_ao_usuario(self, client, auth_headers, test_user):
        # company_id inexistente / sem vínculo deve ser bloqueado
        resp = client.post('/api/sessao/empresa-ativa', json={'company_id': 9999}, headers=auth_headers)
        assert resp.status_code == 403

    def test_define_empresa_ativa_retorna_token(self, client, auth_headers, test_company):
        resp = client.post(
            '/api/sessao/empresa-ativa',
            json={'company_id': test_company.company_id},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['active_company_id'] == test_company.company_id
        assert 'token' in data and data['token']
