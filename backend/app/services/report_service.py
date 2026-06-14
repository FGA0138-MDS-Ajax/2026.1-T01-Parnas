from app.config import db
from app.models import Transaction, Category
from sqlalchemy import func, case
from datetime import date, calendar

class ReportService:

    @staticmethod
    def get_period_summary(company_id, start_date, end_date):
        summary = db.session.query(
            func.sum(case((Transaction.type == 'ENTRADA', Transaction.amount), else_=0)).label('total_receitas'),
            func.sum(case((Transaction.type == 'SAIDA', Transaction.amount), else_=0)).label('total_despesas')
        ).filter(
            Transaction.company_id == company_id,
            Transaction.date.between(start_date, end_date)
        ).first()

        receitas = float(summary.total_receitas or 0)
        despesas = float(summary.total_despesas or 0)
        
        return{
            "total_receitas": receitas,
            "total_despesas": despesas,
            "saldo": receitas - despesas
        }

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
            func.sum(case((Transaction.type == 'ENTRADA', Transaction.amount), else_=-Transaction.amount)).label('fluxo_diario')
        ).filter(
            Transaction.company_id == company_id,
            Transaction.date.between(start_date, end_date)
        ).group_by(Transaction.date).order_by(Transaction.date).all()

        return [{"data": str(trans_date), "valor": float(valor)} for trans_date, valor in results]
    
    @staticmethod
    def get_period_dates(data):

        start = data.get('start_date')
        end = data.get('end_date')
        period = data.get('period')
        month = data.get('month')
        year = data.get('year')
        
        if start and end:
            if start > end:
                raise ValueError("'start_date' não pode ser posterior a 'end_date'.")
            return start, end

        if period == "mensal":
            if not month or not year:
                raise ValueError("Para period=mensal, informe 'month' e 'year'.")
            start = date(year, month, 1)
            end = date(year, month, calendar.monthrange(year, month)[1])
            return start, end

        if period == "anual":
            if not year:
                raise ValueError("Para periodo=anual, informe 'year'.")
            return date(year, 1, 1), date(year, 12, 31)

        raise ValueError(
            "Informe 'period' (mensal ou anual, com 'month'/'year'), "
            "ou informe 'start_date' e 'end_date'."
        )