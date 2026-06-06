from app.config import db
from app.models.simulation import Simulation
from app.models.transaction import Transaction
from models import transaction


def calculate_table_price(main, rate,term ):
    i = rate / 100
    if i == 0:
        pmt = main / term
    else:
        pmt = main*(i * (1 + i)**term) / ((1+i)*(1+i)**term - 1)

    installments = []
    balance_due = main

    for month in range(1,term+1):
        monthly_interest = balance_due * i
        monthly_amortization = pmt - monthly_interest
        balance_due -= monthly_amortization


        #sugestão para front: array installments para montar um gráfico de barras empilhadas ou algo do tipo
        installments.append({
            "mes": month,
            "valor_parcela": round(pmt, 2),
            "amortizacao": round(monthly_amortization, 2),
            "juros": round(monthly_interest, 2),
            "saldo_devedor": round(max(0, balance_due), 2)
        })
    return installments, pmt

def calculate_table_sac(main, rate,term ):
    i = rate / 100
    amortization = main / term
    installments = []
    balance_due = main

    for month in range(1,term+1):
        monthly_interest = balance_due * i
        pmt = amortization + monthly_interest
        balance_due -= amortization

        #sugestão para o front de novo, o sac cai mensalmente, isso é bom para criar um gráfico de linhas decrescente.
        installments.append({
            "mes": month,
            "valor_parcela": round(pmt, 2),
            "amortizacao": round(amortization, 2),
            "juros": round(monthly_interest, 2),
            "saldo_devedor": round(max(0, balance_due), 2)
        })
    return installments, installments[0]["valor_parcela"]

def project_impact_cash_flow(company_id, first_installment_value):
    transactions = Transaction.query.filter_by(company_id=company_id).all()

    if not transactions:
        return {
            "status": "Indisponível",
            "mensagem": "Empresa sem histórico para projeção confiável.",
            "comprometimento_perc": None
        }

    entrys = sum(float(t.amount) for t in transactions if t.typelower() == 'entry')
    exits = sum(float(t.amount) for t in transactions if t.typelower() == 'exits')
    total_profits = entrys - exits

    months_operating = len(set(t.date.strftime('%Y-%m') for t in transactions)) or 1
    avarege_monthly_profit = total_profits / months_operating

    if avarege_monthly_profit <= 0:
        return {
            "status": "Alerta Vermelho",
            "mensagem": "Empresa opera no prejuízo médio. Nova dívida altamente arriscada.",
            "comprometimento_perc": 100.0
        }

    commitment = (first_installment_value / avarege_monthly_profit) * 100
    return {
        "media_lucro_mensal": round(avarege_monthly_profit, 2),
        "comprometimento_perc": round(commitment, 2),
        "status": "Saudável" if commitment <= 30 else "Atenção"
    }