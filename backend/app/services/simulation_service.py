from app.config import db
from app.models.simulation import Simulation
from app.models.transaction import Transaction


def calculate_table_price(main, rate,term ):
    i = rate / 100
    if i == 0:
        pmt = main / term
    else:
        pmt = main * (i * (1 + i) ** term) / ((1 + i) ** term - 1)

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

    entrys = sum(float(t.amount) for t in transactions if t.type.lower() == 'entry')
    exits = sum(float(t.amount) for t in transactions if t.type.lower() == 'exits')
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

def process_simulation(data, company_id=None):
    main = data['requested_amount']
    rate = data['interest_rate']
    term = data['deadline_month']
    modality = data['modality'].upper()

    if modality == 'PRICE':
        installments, base_installments = calculate_table_price(main, rate, term)
    else:
        installments, base_installments = calculate_table_sac(main, rate, term)

    total_payed = sum(p["valor_parcela"] for p in installments)
    total_rate = total_payed - main

    answer = {
        "resumo": {
            "modalidade": modality,
            "valor_solicitado": round(main, 2),
            "total_a_pagar": round(total_payed, 2),
            "total_juros": round(total_rate, 2),
            "primeira_parcela": round(base_installments, 2)
        },
        "detalhamento_mensal": installments
    }

    if company_id:
        answer["projecao_fluxo_caixa"] = project_impact_cash_flow(company_id, base_installments)

    return answer

def save_simulation(data, current_user_id):
    data_simulation = process_simulation(data)
    summary = data_simulation["resumo"]

    new_simulation = Simulation(
        id_empresa=data['company_id'],
        id_usuario=current_user_id,
        valor_solicitado=data['requested_amount'],
        prazo_meses=data['deadline_month'],
        modalidade=data['modality'],
        taxa_juros=data['interest_rate'],
        valor_parcela=summary['primeira_parcela'],
        valor_total=summary['total_a_pagar'],
        total_juros=summary['total_juros']
    )

    try:
        db.session.add(new_simulation)
        db.session.commit()
        return {"mensagem": "Simulação salva no histórico com sucesso.", "id_simulacao": new_simulation.id_simulacao}, 201
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao salvar a simulação."}, 500

def get_simulation(company_id):
    simulations = Simulation.query.filter_by(id_empresa=company_id).all()
    result = []
    for s in simulations:
        result.append({
            "id_simulacao": s.simulation_id,
            "valor_solicitado": float(s.requested_value),
            "prazo_meses": s.deadline_months,
            "modalidade": s.modality,
            "taxa_juros": float(s.interest_rate),
            "valor_parcela": float(s.installment_value),
            "valor_total": float(s.total_value),
            "total_juros": float(s.total_interest),
            "data_simulacao": s.simulation_data.strftime('%Y-%m-%d %H:%M')
        })

    return {"simulations": result}, 200

def delete_simulation(simulation_id, company_id):
    simulation = Simulation.query.filter_by(id_simulacao=simulation_id, id_empresa=company_id).first()

    if not simulation:
        return {"erro": "Simulação não encontrada para esta empresa."}, 404

    try:
        db.session.delete(simulation)
        db.session.commit()
        return {"mensagem": "Simulação excluída com sucesso."}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao excluir a simulação."}, 500