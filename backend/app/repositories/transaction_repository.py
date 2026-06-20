from datetime import date as dt_date
from app.config import db
from app.models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def create(description, amount, date, type, company_id, user_id, category_id):
        """Valor tem que ser positivo"""
        if amount <= 0:
            raise ValueError("O valor da transação deve ser positivo.")

        """Data nao pode ser futura"""
        if date > dt_date.today():
            raise ValueError("A data da transação não pode ser futura.")

        new_transaction = Transaction(
            description=description,
            amount=amount,
            date=date,
            type=type,
            company_id=company_id,
            user_id=user_id,
            category_id=category_id
        )

        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction

    @staticmethod
    def get_by_company(company_id, type=None, category_id=None):
        query = Transaction.query.filter_by(company_id=company_id)

        if type:
            query = query.filter_by(type=type)
        if category_id:
            query = query.filter_by(category_id=category_id)

        return query.order_by(Transaction.date.desc()).all()