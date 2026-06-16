import pytest


@pytest.fixture
def valid_company_payload():
	return {
		"name": "Empresa de Teste LTDA",
		"cnpj": "04.252.011/0001-10",
		"email": "empresa@teste.com",
		"phone": "11999999999",
	}


@pytest.fixture
def payload_without_name(valid_company_payload):
	payload = valid_company_payload.copy()
	payload.pop("name")
	return payload


@pytest.fixture
def payload_without_cnpj(valid_company_payload):
	payload = valid_company_payload.copy()
	payload.pop("cnpj")
	return payload


@pytest.fixture
def payload_with_invalid_cnpj(valid_company_payload):
	payload = valid_company_payload.copy()
	payload["cnpj"] = "11.111.111/1111-11"
	return payload

