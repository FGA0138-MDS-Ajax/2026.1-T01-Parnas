from datetime import date as dt_date
from app.config import db
from app.models.transaction import Transaction
from app.models.category import Category
from sqlalchemy import func

class TransactionRepository:
    model = Transaction

    @staticmethod
    def get_by_id_and_user(transaction_id, user_id):
        return Transaction.query.filter_by(transaction_id=transaction_id, user_id=user_id).first()

    @staticmethod
    def list_by_company_and_user(company_id, user_id):
        return Transaction.query.filter_by(company_id=company_id, user_id=user_id).all()

    @staticmethod
    def get_by_company(company_id, type=None, category_id=None):
        query = Transaction.query.filter_by(company_id=company_id)

        if type:
            query = query.filter_by(type=type)
        if category_id:
            query = query.filter_by(category_id=category_id)

        return query.order_by(Transaction.date.desc()).all()

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
    def get_filtered_history_query(condicoes, categoria_nome=None):
        """Retorna a query base filtrada e os totais agregados."""
        query_base = Transaction.query.filter(*condicoes)
        if categoria_nome:
            query_base = query_base.join(Category).filter(Category.name.ilike(f"%{categoria_nome}%"))

        totais = db.session.query(Transaction.type, func.sum(Transaction.amount)).filter(*condicoes).group_by(Transaction.type).all()
        return query_base, totais

    @staticmethod
    def save(transaction):
        """Salva ou atualiza uma transação existente."""
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def delete_instance(transaction):
        """Remove uma instância de transação do banco."""
        db.session.delete(transaction)
        db.session.commit()