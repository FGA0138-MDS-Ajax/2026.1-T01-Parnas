from app.config import db
from app.models.transaction import Transaction
from app.models.bill import Bill
from app.services.report_service import ReportService
from sqlalchemy import func, case
from datetime import date
import calendar

class DashboardService:

    @staticmethod
    def get_consolidated_balance(company_id):
        summary = db.session.query(
            func.sum(case((func.lower(Transaction.type).in_(['receita', 'entrada']), Transaction.amount), else_=0)).label('total_incomes'),
            func.sum(case((func.lower(Transaction.type).in_(['despesa', 'saida']), Transaction.amount), else_=0)).label('total_expenses')
        ).filter(
            Transaction.company_id == company_id
        ).first()

        # anna: correção para ler os labels idênticos aos definidos na query acima
        incomes = float(summary.total_incomes or 0)
        expenses = float(summary.total_expenses or 0)

        return round(incomes - expenses, 2)

    @staticmethod
    def get_upcoming_bills(company_id):
        today = date.today()
        bills = db.session.query(Bill).filter(
            Bill.company_id == company_id,
            Bill.status == 'Pendente',
            Bill.due_date >= today
        ).order_by(Bill.due_date.asc()).limit(5).all()

        return [
            {
                "id": b.bill_id,
                "descricao": b.description,
                "valor": float(b.amount),
                "data_vencimento": b.due_date.isoformat(),
                "tipo": b.type  # Pagar ou Receber
            } for b in bills
        ]

    @staticmethod
    def build_dashboard(company_id):
        today = date.today()
        last_day = calendar.monthrange(today.year, today.month)[1]
        start_date = date(today.year, today.month, 1)
        end_date = date(today.year, today.month, last_day)

        consolidated_balance = DashboardService.get_consolidated_balance(company_id)

        try:
            monthly_summary = ReportService.get_period_summary(company_id, start_date, end_date)
            category_distribution = ReportService.get_category_distribution(company_id, start_date, end_date)
        except Exception as e:
            print(f"Erro ao acessar ReportService: {e}")
            return {"erro": "Erro ao compilar dados matemáticos do mês atual."}, 500

        pending_bills = DashboardService.get_upcoming_bills(company_id)

        return {
            "saldo_consolidado_atual": consolidated_balance,
            "mes_referencia": today.strftime("%m/%Y"),
            "totais_mes_atual": {
                "receitas": monthly_summary["total_receitas"],
                "despesas": monthly_summary["total_despesas"],
                "balanco_mensal": monthly_summary["saldo"]
            },
            "grafico_categorias_mes": category_distribution,
            "contas_proximas_vencimento": pending_bills
        }, 200