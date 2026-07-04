"""
test_onboarding_flow.py - E2E do onboarding do usuário.

Fluxo de quem chega ao sistema pela primeira vez:
cadastro -> criação da empresa -> seleção da empresa ativa -> consulta e edição
do próprio perfil. Valida que o token emitido no cadastro já autoriza os passos
seguintes e que os dados persistem entre as requisições.
"""

from tests.e2e.helpers import registrar_e_logar, criar_empresa


def test_cadastro_ate_empresa_ativa(client, clean_db):
    headers = registrar_e_logar(client, email="novo@empresa.com")
    company_id = criar_empresa(client, headers, "Minha Empresa")

    # A empresa recém-criada aparece na lista do usuário.
    empresas = client.get("/api/usuarios/me/empresas", headers=headers)
    assert empresas.status_code == 200
    ids = [c["company_id"] for c in empresas.get_json()]
    assert company_id in ids

    # Selecionar a empresa ativa devolve um novo token já com a empresa no contexto.
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

    # Perfil inicial reflete o cadastro.
    antes = client.get("/api/profile", headers=headers)
    assert antes.status_code == 200
    assert antes.get_json()["email"] == "perfil@empresa.com"

    # Edita o nome e a mudança persiste na próxima leitura.
    edicao = client.put("/api/profile", json={"name": "Nome Atualizado"}, headers=headers)
    assert edicao.status_code == 200

    depois = client.get("/api/profile", headers=headers)
    assert depois.get_json()["name"] == "Nome Atualizado"


def test_empresa_ativa_inexistente_e_negada(client, clean_db):
    headers = registrar_e_logar(client, email="semvinculo@empresa.com")

    # Usuário tenta ativar uma empresa que não é dele (ou não existe).
    resp = client.post(
        "/api/sessao/empresa-ativa",
        json={"company_id": 9999},
        headers=headers,
    )

    assert resp.status_code == 403
