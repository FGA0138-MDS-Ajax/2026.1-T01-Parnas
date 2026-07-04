"""E2E do onboarding: cadastro -> empresa -> empresa ativa -> perfil."""

from tests.e2e.helpers import registrar_e_logar, criar_empresa


def test_cadastro_ate_empresa_ativa(client, clean_db):
    headers = registrar_e_logar(client, email="novo@empresa.com")
    company_id = criar_empresa(client, headers, "Minha Empresa")

    empresas = client.get("/api/usuarios/me/empresas", headers=headers)
    assert empresas.status_code == 200
    ids = [c["company_id"] for c in empresas.get_json()]
    assert company_id in ids

    ativa = client.post(
        "/api/sessao/empresa-ativa",
        json={"company_id": company_id},
        headers=headers,
    )
    assert ativa.status_code == 200
    corpo = ativa.get_json()
    assert corpo["active_company_id"] == company_id
    assert "token" in corpo


def test_usuario_edita_o_proprio_perfil(client, clean_db):
    headers = registrar_e_logar(client, email="perfil@empresa.com")

    antes = client.get("/api/profile", headers=headers)
    assert antes.status_code == 200
    assert antes.get_json()["email"] == "perfil@empresa.com"

    edicao = client.put("/api/profile", json={"name": "Nome Atualizado"}, headers=headers)
    assert edicao.status_code == 200

    depois = client.get("/api/profile", headers=headers)
    assert depois.get_json()["name"] == "Nome Atualizado"


def test_empresa_ativa_inexistente_e_negada(client, clean_db):
    headers = registrar_e_logar(client, email="semvinculo@empresa.com")

    resp = client.post(
        "/api/sessao/empresa-ativa",
        json={"company_id": 9999},
        headers=headers,
    )

    assert resp.status_code == 403
