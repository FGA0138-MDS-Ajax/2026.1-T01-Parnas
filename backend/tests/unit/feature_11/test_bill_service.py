# daniel: atualizei para a API atual do BillService - o acesso passou a ser validado por
# _validate_user_company_access (não mais _get_company_id), e as assinaturas viraram
# update_bill(user_id, company_id, bill_id, data), delete_bill(user_id, company_id, bill_id)
# e pay_bill(user_id, company_id, bill_id); o create_bill lê company_id de dentro do data.
from unittest.mock import patch, MagicMock

from app.services.bill_service import BillService


@patch("app.services.bill_service.db")
def test_validate_user_company_access(mock_db):
    # usuário vinculado à empresa 7
    mock_db.session.query.return_value.filter.return_value.first.return_value = MagicMock(
        companies=[MagicMock(company_id=7)]
    )

    assert BillService._validate_user_company_access(1, 7) is True
    assert BillService._validate_user_company_access(1, 99) is False


@patch.object(BillService, "_validate_user_company_access", return_value=True)
@patch("app.services.bill_service.db")
@patch("app.services.bill_service.Bill")
def test_create_bill_persiste_e_retorna_201(mock_bill, mock_db, mock_validate):
    mock_bill.return_value = MagicMock(bill_id=10)
    data = {
        "description": "Luz", "amount": 200.0, "type": "pagar",
        "due_date": "2026-07-01", "category_id": 1, "company_id": 3,
    }

    body, status = BillService.create_bill(user_id=1, data=data)

    assert status == 201
    assert body["id"] == 10
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()


@patch.object(BillService, "_validate_user_company_access", return_value=True)
@patch("app.services.bill_service.Bill")
def test_update_bill_inexistente_retorna_404(mock_bill, mock_validate):
    mock_bill.query.filter_by.return_value.first.return_value = None

    body, status = BillService.update_bill(1, 1, 99, {"description": "x"})

    assert status == 404


@patch.object(BillService, "_validate_user_company_access", return_value=True)
@patch("app.services.bill_service.db")
@patch("app.services.bill_service.Bill")
def test_update_bill_quitada_bloqueia(mock_bill, mock_db, mock_validate):
    mock_bill.query.filter_by.return_value.first.return_value = MagicMock(status="quitado")

    body, status = BillService.update_bill(1, 1, 5, {"description": "x"})

    assert status == 400
    mock_db.session.commit.assert_not_called()


@patch.object(BillService, "_validate_user_company_access", return_value=True)
@patch("app.services.bill_service.Bill")
def test_delete_bill_inexistente_retorna_404(mock_bill, mock_validate):
    mock_bill.query.filter_by.return_value.first.return_value = None

    body, status = BillService.delete_bill(1, 1, 99)

    assert status == 404


@patch.object(BillService, "_validate_user_company_access", return_value=True)
@patch("app.services.bill_service.db")
@patch("app.services.bill_service.Bill")
def test_delete_bill_quitada_bloqueia(mock_bill, mock_db, mock_validate):
    mock_bill.query.filter_by.return_value.first.return_value = MagicMock(status="quitado")

    body, status = BillService.delete_bill(1, 1, 5)

    assert status == 400
    mock_db.session.delete.assert_not_called()


@patch.object(BillService, "_validate_user_company_access", return_value=True)
@patch("app.services.bill_service.Bill")
def test_pay_bill_inexistente_retorna_404(mock_bill, mock_validate):
    mock_bill.query.filter_by.return_value.first.return_value = None

    body, status = BillService.pay_bill(1, 1, 99)

    assert status == 404


@patch.object(BillService, "_validate_user_company_access", return_value=True)
@patch("app.services.bill_service.Bill")
def test_pay_bill_ja_quitada_retorna_400(mock_bill, mock_validate):
    mock_bill.query.filter_by.return_value.first.return_value = MagicMock(status="quitado")

    body, status = BillService.pay_bill(1, 1, 5)

    assert status == 400
