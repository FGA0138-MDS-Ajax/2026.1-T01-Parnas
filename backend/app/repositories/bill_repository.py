from app.config import db
from app.models.bill import Bill
from sqlalchemy.exc import SQLAlchemyError

class BillRepository:

    @staticmethod
    def get_by_status_and_due_date(company_id, status, due_date_start, due_date_end):
        """Lista faturas (bills) por status em um intervalo de datas, ordenadas por vencimento."""
        return Bill.query.filter_by(company_id=company_id, status=status)\
            .filter(Bill.due_date.between(due_date_start, due_date_end))\
            .order_by(Bill.due_date.asc())\
            .all()

    @staticmethod
    def create(data):
        """Cria e persiste uma nova fatura (bill)."""
        try:
            bill = Bill(**data)
            db.session.add(bill)
            db.session.commit()
            return bill
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e 

    @staticmethod
    def update_status(bill_id, status, payment_date):
        """Atualiza o status e a data de quitação de uma fatura existente."""
        bill = Bill.query.get(bill_id)
        if bill:
            try:
                bill.status = status
                bill.payment_date = payment_date
                db.session.commit()
                return bill
            except SQLAlchemyError as e:
                db.session.rollback()
                raise e
        return None