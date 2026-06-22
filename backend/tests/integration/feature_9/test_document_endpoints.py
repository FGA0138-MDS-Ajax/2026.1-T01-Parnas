import io
import pytest

from app.config import db
from app.models.company import Company
from app.services.document_service import DocumentService

URL = "/api/documentos"


@pytest.fixture(autouse=True)
def upload_tmp(tmp_path, monkeypatch):
    """Aponta o storage de uploads para uma pasta temporária do teste."""
    monkeypatch.setattr(DocumentService, "UPLOAD_FOLDER", str(tmp_path))


@pytest.fixture
def empresa_sem_vinculo(test_company):
    """Empresa que NÃO está vinculada ao test_user."""
    company = Company(name="Outra Empresa", cnpj="11.444.777/0001-61",
                    email="outra@empresa.com", phone="1140000000")
    db.session.add(company)
    db.session.commit()
    return company


def _form(company_id, name="Contrato Social", tipo="fiscal", description="Documento fiscal", filename="contrato.pdf", conteudo=b"%PDF-1.4 conteudo"):
    return {
        "file": (io.BytesIO(conteudo), filename),
        "name": name,
        "type": tipo,
        "description": description,
        "company_id": str(company_id),
    }


def _upload(client, headers, company_id, **over):
    return client.post(URL, data=_form(company_id, **over),
                    content_type="multipart/form-data", headers=headers)


def test_upload_documento_valido(client, auth_headers, test_company):
    # Act
    resp = _upload(client, auth_headers, test_company.company_id)

    assert resp.status_code == 201
    body = resp.get_json()
    assert body["name"] == "Contrato Social"
    assert "document_id" in body


def test_upload_sem_arquivo(client, auth_headers, test_company):
    # Act: form sem o campo 'file'
    resp = client.post(
        URL,
        data={"name": "X", "type": "fiscal", "company_id": str(test_company.company_id)},
        content_type="multipart/form-data",
        headers=auth_headers,
    )

    assert resp.status_code == 400
    assert "erro" in resp.get_json()


def test_upload_extensao_nao_permitida(client, auth_headers, test_company):
    # Act: arquivo .exe não é permitido
    resp = _upload(client, auth_headers, test_company.company_id, filename="virus.exe")

    assert resp.status_code == 400


def test_upload_tipo_invalido(client, auth_headers, test_company):
    # Act: type fora de fiscal/contabil/juridico
    resp = _upload(client, auth_headers, test_company.company_id, tipo="outro")

    assert resp.status_code == 400
    assert "erros_de_validacao" in resp.get_json()


def test_upload_sem_nome(client, auth_headers, test_company):
    form = _form(test_company.company_id)
    del form["name"]

    # Act
    resp = client.post(URL, data=form, content_type="multipart/form-data", headers=auth_headers)

    assert resp.status_code == 400
    assert "erros_de_validacao" in resp.get_json()


def test_upload_sem_token(client, test_company):
    # Act
    resp = client.post(URL, data=_form(test_company.company_id), content_type="multipart/form-data")

    assert resp.status_code == 401


def test_upload_empresa_sem_vinculo(client, auth_headers, empresa_sem_vinculo):
    # Act: test_user não está vinculado a esta empresa
    resp = _upload(client, auth_headers, empresa_sem_vinculo.company_id)

    # Assert: acesso negado
    assert resp.status_code == 403


@pytest.mark.xfail(
    reason="DEF: a rota GET chama get_documents_by_company(..., tipo=...), mas o service não aceita "
    "o parâmetro 'tipo' -> TypeError/500 ao listar",
    strict=False,
)
def test_lista_documentos_da_empresa(client, auth_headers, test_company):
    _upload(client, auth_headers, test_company.company_id, name="Balanço", tipo="contabil")

    # Act
    resp = client.get(URL, query_string={"company_id": test_company.company_id}, headers=auth_headers)

    assert resp.status_code == 200
    nomes = [d["name"] for d in resp.get_json()["documentos"]]
    assert "Balanço" in nomes


@pytest.mark.xfail(
    reason="DEF: get_document_for_download chama DocumentRepository.get_by_id, método inexistente "
    "no repository -> AttributeError/500",
    strict=False,
)
def test_download_documento(client, auth_headers, test_company):
    doc_id = _upload(client, auth_headers, test_company.company_id).get_json()["document_id"]

    # Act
    resp = client.get(f"{URL}/{doc_id}/download", headers=auth_headers)

    assert resp.status_code == 200


@pytest.mark.xfail(
    reason="DEF: delete_document chama get_by_id_and_company(document_id, None) com company_id=None; "
    "nunca encontra o documento -> 404 mesmo existindo",
    strict=False,
)
def test_exclui_documento(client, auth_headers, test_company):
    doc_id = _upload(client, auth_headers, test_company.company_id).get_json()["document_id"]

    # Act
    resp = client.delete(f"{URL}/{doc_id}", headers=auth_headers)

    assert resp.status_code == 200
