import pytest
from datetime import date

from app.config import db
from app.models.company import Company
from app.models.category import Category
from app.models.transaction import Transaction

URL = "/api/categories"

CNPJ_A = "11.222.333/0001-81"   # cnpj da test_company
CNPJ_B = "11.444.777/0001-61"   # outra empresa (cnpj válido)
CNPJ_INEXISTENTE = "45.997.418/0001-53"  # válido mas não cadastrado


def _cria(client, headers, cnpj=CNPJ_A, name="Marketing", tipo="despesa"):
    return client.post(URL, json={"name": name, "type": tipo, "cnpj": cnpj}, headers=headers)


@pytest.fixture
def empresa_b():
    company = Company(name="Mercado B", cnpj=CNPJ_B, email="b@empresa.com", phone="1140000000")
    db.session.add(company)
    db.session.commit()
    return company


def test_cria_categoria_dados_validos(client, auth_headers, test_company):
    # Act
    resp = _cria(client, auth_headers, name="Vendas", tipo="receita")

    assert resp.status_code == 201
    assert "msg" in resp.get_json()


def test_cria_categoria_sem_token(client, test_company):
    # Act: sem header de autenticação
    resp = client.post(URL, json={"name": "Vendas", "type": "receita", "cnpj": CNPJ_A})

    assert resp.status_code == 401


def test_cria_categoria_empresa_inexistente(client, auth_headers, clean_db):
    # Act:
    resp = _cria(client, auth_headers, cnpj=CNPJ_INEXISTENTE)

    assert resp.status_code == 404
    assert "erro" in resp.get_json()


def test_cria_categoria_cnpj_invalido(client, auth_headers, test_company):
    # Act: cnpj fora do formato é barrado pelo schema antes do service
    resp = client.post(URL, json={"name": "Vendas", "type": "receita", "cnpj": "123"}, headers=auth_headers)

    assert resp.status_code == 400


def test_lista_categorias_da_empresa(client, auth_headers, test_company):
    _cria(client, auth_headers, name="Vendas", tipo="receita")
    _cria(client, auth_headers, name="Aluguel", tipo="despesa")

    # Act
    resp = client.get(URL, query_string={"cnpj": CNPJ_A}, headers=auth_headers)

    assert resp.status_code == 200
    nomes = {c["name"] for c in resp.get_json()["categories"]}
    assert nomes == {"Vendas", "Aluguel"}


def test_lista_categorias_nao_inclui_de_outra_empresa(client, auth_headers, test_company, empresa_b):
    _cria(client, auth_headers, cnpj=CNPJ_A, name="Vendas A")
    db.session.add(Category(name="Vendas B", type="receita", company_id=empresa_b.company_id))
    db.session.commit()

    # Act: lista pela empresa A
    resp = client.get(URL, query_string={"cnpj": CNPJ_A}, headers=auth_headers)

    nomes = {c["name"] for c in resp.get_json()["categories"]}
    assert nomes == {"Vendas A"}
    assert "Vendas B" not in nomes


def test_atualiza_nome_categoria(client, auth_headers, test_category):
    # Act: edita o nome da categoria existente (test_category = 'Vendas')
    resp = client.put(
        URL,
        json={"id": test_category.category_id, "cnpj": CNPJ_A, "name": "Vendas Online"},
        headers=auth_headers,
    )

    assert resp.status_code == 200
    lista = client.get(URL, query_string={"cnpj": CNPJ_A}, headers=auth_headers).get_json()["categories"]
    assert {c["name"] for c in lista} == {"Vendas Online"}


def test_atualiza_categoria_inexistente(client, auth_headers, test_company):
    # Act
    resp = client.put(URL, json={"id": 9999, "cnpj": CNPJ_A, "name": "X"}, headers=auth_headers)

    assert resp.status_code == 404


def test_exclui_categoria_sem_transacoes(client, auth_headers, test_category):
    # Act
    resp = client.delete(URL, json={"id": test_category.category_id, "cnpj": CNPJ_A}, headers=auth_headers)

    assert resp.status_code == 200
    lista = client.get(URL, query_string={"cnpj": CNPJ_A}, headers=auth_headers).get_json()["categories"]
    assert lista == []


def test_nome_duplicado_nao_permite_segunda(client, auth_headers, test_company):
    _cria(client, auth_headers, name="Vendas", tipo="receita")

    # Act: tenta criar outra com o mesmo nome na mesma empresa
    resp = _cria(client, auth_headers, name="Vendas", tipo="receita")

    # Assert: a constraint UNIQUE(name, company_id) impede a duplicata
    assert resp.status_code != 201
    lista = client.get(URL, query_string={"cnpj": CNPJ_A}, headers=auth_headers).get_json()["categories"]
    assert len(lista) == 1


@pytest.mark.xfail(
    reason="DEF: nome duplicado vaza IntegrityError como 500; o service não valida duplicidade "
    "antes de gravar (deveria responder 400/409)",
    strict=False,
)
def test_nome_duplicado_retorna_status_amigavel(client, auth_headers, test_company):
    _cria(client, auth_headers, name="Vendas", tipo="receita")

    # Act
    resp = _cria(client, auth_headers, name="Vendas", tipo="receita")

    assert resp.status_code in (400, 409)

@pytest.mark.xfail(
    reason="DEF: bloqueio de exclusão de categoria com transações vinculadas não implementado "
    "(tarefa em aberto na issue)",
    strict=False,
)
def test_exclui_categoria_com_transacoes_e_bloqueado(client, auth_headers, test_category, test_user):
    # Arrange: transação vinculada à categoria
    db.session.add(
        Transaction(
            description="Venda",
            amount=100,
            date=date(2025, 5, 1),
            type="receita",
            company_id=test_category.company_id,
            user_id=test_user.user_id,
            category_id=test_category.category_id,
        )
    )
    db.session.commit()

    # Act
    resp = client.delete(URL, json={"id": test_category.category_id, "cnpj": CNPJ_A}, headers=auth_headers)

    # Assert: deveria recusar a exclusão por haver transação vinculada
    assert resp.status_code in (400, 409)


@pytest.mark.xfail(
    reason="DEF: service ignora o user_id do JWT; qualquer usuário autenticado gerencia categorias "
    "de qualquer empresa pelo cnpj, sem checar o vínculo user_company",
    strict=False,
)
def test_usuario_sem_vinculo_nao_gerencia_categoria_de_outra_empresa(client, auth_headers, test_company, empresa_b):
    # Act: test_user não está vinculado à empresa B, mas tenta criar categoria nela
    resp = _cria(client, auth_headers, cnpj=CNPJ_B, name="Indevida")

    assert resp.status_code == 403
