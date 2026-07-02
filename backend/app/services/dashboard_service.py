from app.repositories.company_repository import CompanyRepository
from app.services.report_service import ReportService
from app.exceptions.api_exception import APIException
from app.models.transaction import Transaction
from sqlalchemy import func, case
from app.models.bill import Bill
from datetime import date
from app.config import db
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

        incomes = float(summary.total_incomes or 0)
        expenses = float(summary.total_expenses or 0)

        return round(incomes - expenses, 2)


    @staticmethod
    def get_upcoming_bills(company_id):
        today = date.today()
        #anna - correção: func.lower() para ignorar diferenças de caixa alta/baixa com o SQLite
        bills = db.session.query(Bill).filter(
            Bill.company_id == company_id,
            func.lower(Bill.status) == 'pendente',
            Bill.due_date >= today
        ).order_by(Bill.due_date.asc()).limit(5).all()

        def normalizar_tipo(tipo):
            if not tipo:
                return tipo
            t = tipo.lower()
            if t == 'pagar':
                return 'Pagar'
            if t == 'receber':
                return 'Receber'
            return tipo.capitalize()

        return [
            {
                "id": b.bill_id,
                "descricao": b.description,
                "valor": float(b.amount),
                "data_vencimento": b.due_date.isoformat(),
                "tipo": normalizar_tipo(b.type),
            } for b in bills
        ]


    @staticmethod
    def build_dashboard(user_id, company_id):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)
        
        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
        
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
            return {"erro": f"Erro ao compilar dados matemáticos do mês atual: {str(e)}"}, 500

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