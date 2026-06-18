import pytest
from unittest.mock import patch, MagicMock
from app.services.company_service import delete_company


@patch('app.services.company_service.db')
@patch('app.services.company_service.find_company')
def test_delete_company_success_by_owner(mock_find_company, mock_db):
    """Cobre o Critério: Gestor consegue excluir a empresa e todos os dados vinculados"""

    # 1. Simula que a empresa foi encontrada no banco
    mock_company = MagicMock(company_id=1, cnpj="04252011000110")
    mock_find_company.return_value = mock_company

    # 2. Simula que a query que verifica o vínculo (user_company) retornou True (o usuário tem acesso)
    mock_db.session.query.return_value.filter.return_value.first.return_value = True

    # 3. Chama a função real
    response, status_code = delete_company(cnpj="04.252.011/0001-10", user_id=42)

    # 4. Verifica se a resposta foi de sucesso
    assert status_code == 200
    assert response["mensagem"] == "Empresa excluída com sucesso."

    # 5. Verifica se o SQLAlchemy recebeu o comando de deletar o objeto (o que aciona os cascades)
    mock_db.session.delete.assert_called_once_with(mock_company)
    mock_db.session.commit.assert_called_once()


@patch('app.services.company_service.db')
@patch('app.services.company_service.find_company')
def test_delete_company_rejects_if_not_owner(mock_find_company, mock_db):
    """Cobre o Critério: Usuário não consegue excluir empresa se não for o responsável"""

    # 1. Simula que a empresa existe
    mock_company = MagicMock(company_id=1)
    mock_find_company.return_value = mock_company

    # 2. Simula que a query de vínculo retornou None (o usuário NÃO pertence à empresa)
    mock_db.session.query.return_value.filter.return_value.first.return_value = None

    # 3. Chama a função com um usuário sem permissão
    response, status_code = delete_company(cnpj="04.252.011/0001-10", user_id=99)

    # 4. Verifica a falha de segurança
    assert status_code == 403
    assert "Acesso negado" in response["erro"]

    # 5. Garante que o banco NÃO foi alterado
    mock_db.session.delete.assert_not_called()