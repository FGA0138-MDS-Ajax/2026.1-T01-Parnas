from app.config import db
from app.models import Transaction, Category
from sqlalchemy import func, case
from app.models.company import Company
from app.models.user_company_association import user_company
from datetime import date
import calendar
import re

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

def generate_report(user_id, data):
    cnpj = data.get('cnpj')
    cnpj_clean = re.sub(r'\D', '', cnpj)
    company = db.session.query(Company).filter(Company.cnpj==cnpj_clean).first()

    if not company:
        return {"erro": "Empresa não encontrada."}, 404

    has_access = db.session.query(user_company).filter(
        user_company.c.user_id == user_id,
        user_company.c.company_id == company.company_id
    ).first()

    if not has_access:
        return {"erro": "Acesso negado. Você não tem permissão para acessar os relatórios dessa empresa!"}, 403

    try:
        start_date, end_date = ReportService.get_period_dates(data)
    except ValueError as e:
        return {"erro": str(e)}, 400

    try:
        totais = ReportService.get_period_summary(company.company_id, start_date, end_date)
        distribuicao = ReportService.get_category_distribution(company.company_id, start_date, end_date)
        evolucao = ReportService.get_balance_evolution(company.company_id, start_date, end_date)
    except Exception as e:
        print(f"Erro ao gerar relatório financeiro: {str(e)}")
        return {"erro": "Ocorreu um erro interno ao gerar o relatório."}, 500

    return {
        "periodo": {
            "data_inicio": start_date.isoformat(),
            "data_fim": end_date.isoformat(),
        },
        "totais": totais,
        "distribuicao_categorias": distribuicao,
        "evolucao": evolucao,
    }, 200
