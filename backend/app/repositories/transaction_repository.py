from datetime import date as dt_date
from app.config import db
from app.models.transaction import Transaction
from app.models.category import Category
from sqlalchemy import func
from app.repositories.base_repository import BaseRepository
from sqlalchemy import func, case


class TransactionRepository(BaseRepository):
    
    _base = BaseRepository(Transaction)
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
    def get_by_date_range(company_id, start_date, end_date):
        return Transaction.query.filter(
            Transaction.company_id == company_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).order_by(Transaction.date.desc()).all()
    
    @staticmethod
    def create(description, amount, date, type, company_id, user_id, category_id):
        if amount <= 0:
            raise ValueError("O valor da transação deve ser positivo.")
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
        return TransactionRepository._base.save(new_transaction)
    
    @staticmethod
    def get_filtered_history_query(filtros, categoria_nome=None):
        query_base = Transaction.query.filter_by(
            user_id=filtros.get('user_id'),
            company_id=filtros.get('company_id')
        )
        
        if filtros.get('data_inicio'):
            query_base = query_base.filter(Transaction.date >= filtros['data_inicio'])
        if filtros.get('data_fim'):
            query_base = query_base.filter(Transaction.date <= filtros['data_fim'])
        if filtros.get('tipo'):
            query_base = query_base.filter_by(type=filtros['tipo'])
        if filtros.get('valor_min') is not None:
            query_base = query_base.filter(Transaction.amount >= filtros['valor_min'])
        if filtros.get('valor_max') is not None:
            query_base = query_base.filter(Transaction.amount <= filtros['valor_max'])
        if categoria_nome:
            query_base = query_base.join(Category).filter(Category.name.ilike(f"%{categoria_nome}%"))
        
        totais = db.session.query(Transaction.type, func.sum(Transaction.amount)).filter(
            Transaction.user_id == filtros.get('user_id'),
            Transaction.company_id == filtros.get('company_id')
        )
        if filtros.get('data_inicio'):
            totais = totais.filter(Transaction.date >= filtros['data_inicio'])
        if filtros.get('data_fim'):
            totais = totais.filter(Transaction.date <= filtros['data_fim'])
        if filtros.get('tipo'):
            totais = totais.filter_by(type=filtros['tipo'])
        if filtros.get('valor_min') is not None:
            totais = totais.filter(Transaction.amount >= filtros['valor_min'])
        if filtros.get('valor_max') is not None:
            totais = totais.filter(Transaction.amount <= filtros['valor_max'])
        if categoria_nome:
            totais = totais.join(Category).filter(Category.name.ilike(f"%{categoria_nome}%"))
        totais = totais.group_by(Transaction.type).all()
        
        return query_base, totais
    
    @staticmethod
    def save(transaction):
        return TransactionRepository._base.save(transaction)
    
    @staticmethod
    def get_category_distribution(company_id, start_date, end_date):
        results = db.session.query(
            Category.name, 
            func.sum(Transaction.amount).label('total')
        ).join(Transaction).filter(
            Transaction.company_id == company_id,
            Transaction.type == 'SAIDA',
            Transaction.date.between(start_date, end_date)
        ).group_by(Category.name).all()
        
        return [{"categoria": name, "total": float(total)} for name, total in results]
    
    @staticmethod
    def get_balance_evolution(company_id, start_date, end_date):
        results = db.session.query(
            Transaction.date,
            func.sum(case(
                (Transaction.type == 'ENTRADA', Transaction.amount),
                else_=-Transaction.amount
            )).label('fluxo_diario')
        ).filter(
            Transaction.company_id == company_id,
            Transaction.date.between(start_date, end_date)
        ).group_by(Transaction.date).order_by(Transaction.date).all()
        
        return [{"data": str(trans_date), "valor": float(valor)} for trans_date, valor in results]
    
    @staticmethod
    def delete_instance(transaction):
        TransactionRepository._base.delete(transaction)