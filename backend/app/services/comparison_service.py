from app.models.comparison import Comparison, ComparisonModality
from app.config import db
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from flask_jwt_extended import get_jwt

from app.exceptions.api_exception import APIException
from app.repositories.company_repository import CompanyRepository # Nova importação necessária!


class ComparisonService:

    @staticmethod
    def _calculate_price_table(loan_amount, rate_percent, term_months):
        """Calcula a matemática financeira da Tabela Price"""
        amount = float(loan_amount)
        rate = float(rate_percent) / 100.0
        term = int(term_months)

        if rate == 0:
            pmt = amount / term
            total = amount
        else:
            # Fórmula Tabela Price
            pmt = amount * (rate * (1 + rate) ** term) / ((1 + rate) ** term - 1)
            total = pmt * term

        interest = total - amount
        return round(pmt, 2), round(total, 2), round(interest, 2)


    @staticmethod
    def calculate_simulation(user_id, company_id, data):

        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)


        """Apenas calcula e retorna os dados formatados (não salva no banco)"""
        loan_amount = data.get('loan_amount', 0)
        modalities = data.get('modalities', [])

        if not modalities or len(modalities) > 4:
            return {"erro": "Forneça entre 1 e 4 modalidades para comparar."}, 400

        results = []
        lowest_total = float('inf')
        best_modality_index = -1

        for idx, mod in enumerate(modalities):
            pmt, total, interest = ComparisonService._calculate_price_table(
                loan_amount, mod['interest_rate'], mod['term_months']
            )

            # Regra de Negócio: Identifica a mais vantajosa (menor custo total)
            if total < lowest_total:
                lowest_total = total
                best_modality_index = idx

            results.append({
                "name": mod['name'],
                "interest_rate": mod['interest_rate'],
                "term_months": mod['term_months'],
                "type": mod['type'].upper(),
                "monthly_payment": pmt,
                "total_amount": total,
                "total_interest": interest,
                "is_best_option": False,
                # Regra de Negócio: Alerta sobre o uso de crédito PF
                "warning_pf": mod['type'].upper() == 'PF'
            })

        if best_modality_index != -1:
            results[best_modality_index]["is_best_option"] = True

        return {"loan_amount": loan_amount, "comparisons": results}, 200


    @staticmethod
    def save_comparison(user_id, company_id, data):
        """Calcula e salva as métricas no banco de dados"""

        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
        
        # Faz o cálculo reutilizando o método acima
        simulacao_result, status = ComparisonService.calculate_simulation(user_id, company_id, data)
        if status != 200:
            return simulacao_result, status

        # 1. Salva o cabeçalho da comparação
        nova_comparacao = Comparison(
            company_id=company_id,
            user_id=user_id,
            loan_amount=simulacao_result['loan_amount']
        )
        db.session.add(nova_comparacao)
        db.session.flush()

        # 2. Salva as modalidades calculadas
        for mod in simulacao_result['comparisons']:
            nova_modalidade = ComparisonModality(
                comparison_id=nova_comparacao.comparison_id,
                name=mod['name'],
                interest_rate=mod['interest_rate'],
                term_months=mod['term_months'],
                type=mod['type'],
                monthly_payment=mod['monthly_payment'],
                total_amount=mod['total_amount'],
                total_interest=mod['total_interest']
            )
            db.session.add(nova_modalidade)

        db.session.commit()
        return {"mensagem": "Comparação salva com sucesso!", "id": nova_comparacao.comparison_id}, 201


    @staticmethod
    def get_comparisons(user_id, company_id):

        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

        comparacoes = Comparison.query.filter_by(company_id=company_id).order_by(Comparison.created_at.desc()).all()

        resultado = []
        for comp in comparacoes:
            resultado.append({
                "id": comp.comparison_id,
                "created_at": comp.created_at.isoformat(),
                "loan_amount": float(comp.loan_amount),
                "modalities": [{
                    "name": m.name,
                    "monthly_payment": float(m.monthly_payment),
                    "total_amount": float(m.total_amount),
                    "type": m.type
                } for m in comp.modalities]
            })

        return resultado, 200


    @staticmethod
    def delete_comparison(user_id, company_id, comparison_id):

        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
        
        comparacao = Comparison.query.filter_by(comparison_id=comparison_id, company_id=company_id).first()

        if not comparacao:
            return {"erro": "Comparação não encontrada"}, 404

        db.session.delete(comparacao)
        db.session.commit()
        return {"mensagem": "Comparação excluída com sucesso"}, 200


    @staticmethod
    def generate_pdf_report(user_id, company_id, comparison_id):
        """Gera um PDF em memória com os dados da comparação"""
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
        
        comparacao = Comparison.query.filter_by(comparison_id=comparison_id, company_id=company_id).first()

        if not comparacao:
            return None, 404

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setTitle(f"Relatório de Crédito #{comparison_id}")

        # Título
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, f"Comparativo de Modalidades de Crédito")

        c.setFont("Helvetica", 10)
        c.drawString(50, 730, f"Data da Simulação: {comparacao.created_at.strftime('%d/%m/%Y')}")

        y_position = 680
        for m in comparacao.modalities:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_position, f"Modalidade: {m.name} ({m.type.upper()})")

            c.setFont("Helvetica", 10)
            y_position -= 20
            c.drawString(70, y_position, f"Taxa de Juros: {m.interest_rate}% a.m. | Prazo: {m.term_months} meses")
            y_position -= 20
            c.drawString(70, y_position, f"Valor da Parcela: R$ {m.monthly_payment:,.2f}")
            y_position -= 20
            c.drawString(70, y_position, f"Custo Total: R$ {m.total_amount:,.2f} (Juros: R$ {m.total_interest:,.2f})")

            y_position -= 40  # Espaço para o próximo bloco

        c.save()
        buffer.seek(0)
        return buffer, 200