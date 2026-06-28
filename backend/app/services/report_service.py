import calendar
from datetime import date
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository


def _get_company_id(user_id):
    user = UserRepository.get_by_id(user_id)
    return user.active_company_id if user else None


def get_period_summary(company_id, start_date, end_date):
    transactions = TransactionRepository.get_by_date_range(company_id, start_date, end_date)

    receitas = sum(float(t.amount) for t in transactions if t.type.lower() == 'receita')
    despesas = sum(float(t.amount) for t in transactions if t.type.lower() == 'despesa')

    return {
        "total_receitas": receitas,
        "total_despesas": despesas,
        "saldo": receitas - despesas
    }


def get_category_distribution(company_id, start_date, end_date):
    return TransactionRepository.get_category_distribution(company_id, start_date, end_date)


def get_balance_evolution(company_id, start_date, end_date):
    return TransactionRepository.get_balance_evolution(company_id, start_date, end_date)


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
    company_id = _get_company_id(user_id)

    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    try:
        start_date, end_date = get_period_dates(data)
    except ValueError as e:
        return {"erro": str(e)}, 400

    try:
        totais = get_period_summary(company_id, start_date, end_date)
        distribuicao = get_category_distribution(company_id, start_date, end_date)
        evolucao = get_balance_evolution(company_id, start_date, end_date)
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