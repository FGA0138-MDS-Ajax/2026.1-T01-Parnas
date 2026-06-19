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
            func.sum(case((Transaction.type == 'ENTRADA', Transaction.amount), else_=0)).label('total_receitas'),
            func.sum(case((Transaction.type == 'SAIDA', Transaction.amount), else_=0)).label('total_despesas')
        ).filter(
            Transaction.company_id == company_id
        ).first()

        receitas = float(summary.total_receitas or 0)
        despesas = float(summary.total_despesas or 0)

        return round(receitas - despesas, 2)

    @staticmethod
    def get_upcoming_bills(company_id):
        hoje = date.today()
        bills = db.session.query(Bill).filter(
            Bill.company_id == company_id,
            Bill.status == 'Pendente',
            Bill.due_date >= hoje
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

def build_dashboard(company_id):
    hoje = date.today()
    ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
    start_date = date(hoje.year, hoje.month, 1)
    end_date = date(hoje.year, hoje.month, ultimo_dia)

    saldo_consolidado = DashboardService.get_consolidated_balance(company_id)

    try:
        resumo_mensal = ReportService.get_period_summary(company_id, start_date, end_date)
        distribuicao_categorias = ReportService.get_category_distribution(company_id, start_date, end_date)
    except Exception as e:
        print(f"Erro ao acessar ReportService: {e}")
        return {"erro": "Erro ao compilar dados matemáticos do mês atual."}, 500

    contas_pendentes = DashboardService.get_upcoming_bills(company_id)

    return {
        "saldo_consolidado_atual": saldo_consolidado,
        "mes_referencia": hoje.strftime("%m/%Y"),
        "totais_mes_atual": {
            "receitas": resumo_mensal["total_receitas"],
            "despesas": resumo_mensal["total_despesas"],
            "balanco_mensal": resumo_mensal["saldo"]
        },
        "grafico_categorias_mes": distribuicao_categorias,
        "contas_proximas_vencimento": contas_pendentes
    }, 200