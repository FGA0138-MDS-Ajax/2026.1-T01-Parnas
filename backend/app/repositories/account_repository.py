from app.config import db
from app.models.account import Account
from sqlalchemy.exc import SQLAlchemyError

class AccountRepository:

    @staticmethod
    def get_by_status_and_due_date(company_id, status, due_date_start, due_date_end):
        """Lista contas por status em um intervalo de datas, ordenadas pela data de vencimento."""
        return Account.query.filter_by(company_id=company_id, status=status)\
            .filter(Account.due_date.between(due_date_start, due_date_end))\
            .order_by(Account.due_date.asc())\
            .all()

    @staticmethod
    def create(data):
        """Cria e persiste uma nova conta."""
        try:
            account = Account(**data)
            db.session.add(account)
            db.session.commit()
            return account
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e 

    @staticmethod
    def update_status(account_id, status, payment_date):
        """Atualiza o status e a data de quitação de uma conta existente."""
        account = Account.query.get(account_id)
        if account:
            try:
                account.status = status
                account.payment_date = payment_date
                db.session.commit()
                return account
            except SQLAlchemyError as e:
                db.session.rollback()
                raise e
        return None