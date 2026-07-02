from app.repositories.simulation_repository import SimulationRepository
from app.repositories.transaction_repository import TransactionRepository
from app.exceptions.api_exception import APIException
from app.repositories.company_repository import CompanyRepository

class SimulationService:
    @staticmethod
    def calculate_table_price(main, rate, term):
        i = rate/100
        if i==0:
            pmt = main/term
        else:
            pmt = main*(i*(1+i)**term)/((1+i)**term-1)

        installments = []
        balance_due = main

        for month in range(1,term+1):
            monthly_interest = balance_due*i
            monthly_amortization = pmt-monthly_interest
            balance_due -= monthly_amortization

            installments.append({
                "mes": month,
                "valor_parcela": round(pmt, 2),
                "amortizacao": round(monthly_amortization, 2),
                "juros": round(monthly_interest, 2),
                "saldo_devedor": round(max(0, balance_due), 2)
            })

        return installments, pmt


    @staticmethod
    def calculate_table_sac(main, rate, term):
        i = rate/100
        amortization = main/term
        balance_due = main
        installments = []

        for month in range(1,term+1):
            monthly_interest = balance_due*i
            pmt = amortization + monthly_interest
            balance_due -= amortization

            installments.append({
                "mes": month,
                "valor_parcela": round(pmt, 2),
                "amortizacao": round(amortization, 2),
                "juros": round(monthly_interest, 2),
                "saldo_devedor": round(max(0, balance_due), 2)
            })

        return installments, installments[0]["valor_parcela"]


    @staticmethod
    def project_impact_cash_flow(company_id, first_installment_value):
        transactions = TransactionRepository.get_by_company(company_id)
        if not transactions:
            return {
                "status": "Indisponível",
                "mensagem": "Empresa sem histórico para projeção confiável.",
                "comprometimento_perc": None
            }

        entries = sum(float(t.amount) for t in transactions if t.type.lower() == 'receita')
        exits = sum(float(t.amount) for t in transactions if t.type.lower() == 'despesa')
        total_profits = entries - exits

        months_operating = len(set(t.date.strftime("%Y-%m") for t in transactions)) or 1
        average_monthly_profit = total_profits/months_operating

        if average_monthly_profit <= 0:
            return {
                "status": "Alerta vermelho",
                "mensagem": "Empresa opera no prejuízo médio. Nova dívida altamente arriscada",
                "comprometimento_perc": 100.0
            }

        commitment = (first_installment_value/average_monthly_profit)*100

        return{
            "media_lucro_mensal": round(average_monthly_profit, 2),
            "comprometimento_perc": round(commitment, 2),
            "status": "Saudável" if commitment <= 30 else "Atenção"
        }


    @staticmethod
    def process_simulation(user_id, company_id, data):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
        
        main = data['requested_amount']
        rate = data['interest_rate']
        term = data['deadline_month']
        modality = data['modality'].upper()

        if modality == 'PRICE':
            installments, base_installment = SimulationService.calculate_table_price(main, rate, term)
        else:
            installments, base_installment = SimulationService.calculate_table_sac(main, rate, term)

        total_paid = sum(p["valor_parcela"] for p in installments)
        total_interest = total_paid - main

        answer = {
            "resumo": {
                "modalidade": modality,
                "valor_solicitado": round(main, 2),
                "total_a_pagar": round(total_paid, 2),
                "total_juros": round(total_interest, 2),
                "primeira_parcela": round(base_installment, 2)
            },
            "detalhamento_mensal": installments,
            "projecao_fluxo_caixa": SimulationService.project_impact_cash_flow(company_id, base_installment)
        }

        return answer


    @staticmethod
    def save_simulation(user_id, company_id, data):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

        data_simulation = SimulationService.process_simulation(user_id, company_id, data)
        summary = data_simulation["resumo"]

        try:
            new_simulation = SimulationRepository.create(
                company_id=company_id,
                user_id=user_id,
                loan_amount=data['requested_amount'],
                term_months=data['deadline_month'],
                modality=data['modality'],
                interest_rate=data['interest_rate'],
                monthly_payment=summary['primeira_parcela'],
                total_amount=summary['total_a_pagar'],
                total_interest=summary['total_juros']
            )
            return {"mensagem": "Simulação salva no histórico com sucesso.",
                    "simulation_id": new_simulation.simulation_id}, 201
        except Exception as e:
            return {"erro": f"Ocorreu um erro interno ao salvar a simulação: {str(e)}"}, 500


    @staticmethod
    def get_simulation(user_id, company_id):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

        simulations = SimulationRepository.list_by_company(company_id)
        result = []
        for s in simulations:
            result.append({
                "simulation_id": s.simulation_id,
                "valor_solicitado": float(s.loan_amount),
                "prazo_meses": s.term_months,
                "modalidade": s.modality,
                "taxa_juros": float(s.interest_rate),
                "valor_parcela": float(s.monthly_payment),
                "valor_total": float(s.total_amount),
                "total_juros": float(s.total_interest),
                "data_simulacao": s.created_at.strftime('%Y-%m-%d %H:%M')
            })

        return {"simulations": result}, 200


    @staticmethod
    def delete_simulation(user_id, company_id, simulation_id):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
        
        simulation = SimulationRepository.get_by_id_and_company(simulation_id, company_id)
        if not simulation:
            raise APIException("Simulação não encontrada para esta empresa.", 404)

        try:
            SimulationRepository.delete(simulation)
            return {"mensagem": "Simulação excluída com sucesso."}, 200
        except Exception as e:
            return {"erro": f"Ocorreu um erro interno ao tentar excluir a simulação: {str(e)}"}, 500