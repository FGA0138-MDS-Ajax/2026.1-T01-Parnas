from app.config import db
from app.models.bill import Bill
from sqlalchemy.exc import SQLAlchemyError

class BillRepository:
    model = Bill

    @staticmethod
    def get_by_id_and_company(bill_id, company_id):
        return Bill.query.filter_by(bill_id=bill_id, company_id=company_id).first()

    @staticmethod
    def list_by_company(company_id, status=None):
        query = Bill.query.filter_by(company_id=company_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Bill.due_date.asc()).all()

    @staticmethod
    def get_by_status_and_due_date(company_id, status, due_date_start, due_date_end):
        return Bill.query.filter_by(company_id=company_id, status=status)\
            .filter(Bill.due_date.between(due_date_start, due_date_end))\
            .order_by(Bill.due_date.asc())\
            .all()

    @staticmethod
    def create(company_id, description, amount, type, due_date, category_id):
        bill = Bill(
            company_id=company_id,
            description=description,
            amount=amount,
            type=type,
            due_date=due_date,
            category_id=category_id
        )
        db.session.add(bill)
        db.session.commit()
        return bill

    @staticmethod
    def save(bill):
        db.session.add(bill)
        db.session.commit()
        return bill

    @staticmethod
    def delete(bill):
        db.session.delete(bill)
        db.session.commit()