# daniel: delete_company virou delete_company(company_id, user_id) via CompanyRepository;
# mocko o repositorio (nao mais find_company) e a falta de acesso levanta APIException(403).
import pytest
from unittest.mock import MagicMock
from app.services.company_service import delete_company
from app.exceptions.api_exception import APIException


def test_delete_company_success_by_owner(mocker):
    """Cobre o Critério: Gestor consegue excluir a empresa e todos os dados vinculados"""

    repo = mocker.patch('app.services.company_service.CompanyRepository')

    # 1. Empresa encontrada
    mock_company = MagicMock(company_id=1, cnpj="04252011000110")
    repo.get_by_id.return_value = mock_company
    # 2. Acesso liberado (check_access não levanta)
    repo.check_access.return_value = None

    # 3. Chama a função real
    response, status_code = delete_company(company_id=1, user_id=42)

    # 4. Resposta de sucesso
    assert status_code == 200
    assert response["mensagem"] == "Empresa deletada com sucesso."

    # 5. Verifica acesso e deleção pelo repositório
    repo.check_access.assert_called_once_with(1, 42)
    repo.delete.assert_called_once_with(1)


