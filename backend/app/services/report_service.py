import calendar
from datetime import date
from app.repositories.transaction_repository import TransactionRepository
from app.exceptions.api_exception import APIException
from app.repositories.company_repository import CompanyRepository

class ReportService:
    @staticmethod
    def get_period_summary(company_id, start_date, end_date):
        transactions = TransactionRepository.get_by_date_range(company_id, start_date, end_date)

        receitas = sum(float(t.amount) for t in transactions if t.type.lower() == 'receita')
        despesas = sum(float(t.amount) for t in transactions if t.type.lower() == 'despesa')

        return {
            "total_receitas": receitas,
            "total_despesas": despesas,
            "saldo": receitas - despesas
        }


    @staticmethod
    def get_category_distribution(company_id, start_date, end_date):
        return TransactionRepository.get_category_distribution(company_id, start_date, end_date)


    @staticmethod
    def get_balance_evolution(company_id, start_date, end_date):
        return TransactionRepository.get_balance_evolution(company_id, start_date, end_date)


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


    @staticmethod
    def generate_report(user_id,company_id, data):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

        try:
            start_date, end_date = ReportService.get_period_dates(data)
        except ValueError as e:
            return {"erro": str(e)}, 400

        try:
            totais = ReportService.get_period_summary(company_id, start_date, end_date)
            distribuicao = ReportService.get_category_distribution(company_id, start_date, end_date)
            evolucao = ReportService.get_balance_evolution(company_id, start_date, end_date)
        except Exception as e:
            print(f"Erro ao gerar relatório financeiro: {str(e)}")
            return {"erro": f"Ocorreu um erro interno ao gerar o relatório: {str(e)}"}, 500

        return {
            "periodo": {
                "data_inicio": start_date.isoformat(),
                "data_fim": end_date.isoformat(),
            },
            "totais": totais,
            "distribuicao_categorias": distribuicao,
            "evolucao": evolucao,
        }, 200