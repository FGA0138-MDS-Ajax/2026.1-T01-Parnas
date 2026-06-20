from unittest.mock import patch, MagicMock

from app.services.bill_service import BillService


@patch("app.services.bill_service.User")
def test_get_company_id_retorna_empresa_do_usuario(mock_user):
    mock_user.query.get.return_value = MagicMock(company_id=7)

    assert BillService._get_company_id(1) == 7


@patch("app.services.bill_service.db")
@patch("app.services.bill_service.Bill")
@patch("app.services.bill_service.User")
def test_create_bill_persiste_e_retorna_201(mock_user, mock_bill, mock_db):
    mock_user.query.get.return_value = MagicMock(company_id=3)
    mock_bill.return_value = MagicMock(bill_id=10)
    data = {
        "description": "Luz", "amount": 200.0, "type": "pagar",
        "due_date": "2026-07-01", "category_id": 1,
    }

    body, status = BillService.create_bill(user_id=1, data=data)

    assert status == 201
    assert body["id"] == 10
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()


@patch("app.services.bill_service.Bill")
@patch("app.services.bill_service.User")
def test_update_bill_inexistente_retorna_404(mock_user, mock_bill):
    mock_user.query.get.return_value = MagicMock(company_id=1)
    mock_bill.query.filter_by.return_value.first.return_value = None

    body, status = BillService.update_bill(1, 99, {"description": "x"})

    assert status == 404


@patch("app.services.bill_service.db")
@patch("app.services.bill_service.Bill")
@patch("app.services.bill_service.User")
def test_update_bill_quitada_bloqueia(mock_user, mock_bill, mock_db):
    mock_user.query.get.return_value = MagicMock(company_id=1)
    mock_bill.query.filter_by.return_value.first.return_value = MagicMock(status="quitado")

    body, status = BillService.update_bill(1, 5, {"description": "x"})

    assert status == 400
    mock_db.session.commit.assert_not_called()


@patch("app.services.bill_service.Bill")
@patch("app.services.bill_service.User")
def test_delete_bill_inexistente_retorna_404(mock_user, mock_bill):
    mock_user.query.get.return_value = MagicMock(company_id=1)
    mock_bill.query.filter_by.return_value.first.return_value = None

    body, status = BillService.delete_bill(1, 99)

    assert status == 404


@patch("app.services.bill_service.db")
@patch("app.services.bill_service.Bill")
@patch("app.services.bill_service.User")
def test_delete_bill_quitada_bloqueia(mock_user, mock_bill, mock_db):
    mock_user.query.get.return_value = MagicMock(company_id=1)
    mock_bill.query.filter_by.return_value.first.return_value = MagicMock(status="quitado")

    body, status = BillService.delete_bill(1, 5)

    assert status == 400
    mock_db.session.delete.assert_not_called()


@patch("app.services.bill_service.Bill")
@patch("app.services.bill_service.User")
def test_pay_bill_inexistente_retorna_404(mock_user, mock_bill):
    mock_user.query.get.return_value = MagicMock(company_id=1)
    mock_bill.query.filter_by.return_value.first.return_value = None

    body, status = BillService.pay_bill(1, 99)

    assert status == 404


@patch("app.services.bill_service.Bill")
@patch("app.services.bill_service.User")
def test_pay_bill_ja_quitada_retorna_400(mock_user, mock_bill):
    mock_user.query.get.return_value = MagicMock(company_id=1)
    mock_bill.query.filter_by.return_value.first.return_value = MagicMock(status="quitado")

    body, status = BillService.pay_bill(1, 5)

    assert status == 400
