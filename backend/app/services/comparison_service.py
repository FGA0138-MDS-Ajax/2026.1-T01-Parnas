from app.repositories.company_repository import CompanyRepository
from app.models.comparison import Comparison, ComparisonModality
from app.exceptions.api_exception import APIException
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from app.config import db
from datetime import datetime
import io


def _fmt_currency(value):
    texto = f"{float(value):,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"

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
            raise APIException("Forneça entre 1 e 4 modalidades para comparar.", 400)

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
        try:
            simulacao_result, status = ComparisonService.calculate_simulation(user_id, company_id, data)
            if status != 200:
                return simulacao_result, status
        except Exception as e:
            raise APIException(f"Erro ao calcular simulação: {str(e)}", 500)

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
            # Lógica para encontrar a melhor modalidade (menor custo total)
            best_modality = None
            lowest_total = float('inf')
            
            for m in comp.modalities:
                if m.total_amount < lowest_total:
                    lowest_total = m.total_amount
                    best_modality = m
            
            if not best_modality and comp.modalities:
                best_modality = comp.modalities[0]

            resultado.append({
                "id": comp.comparison_id,
                "created_at": comp.created_at.isoformat(),
                "loan_amount": float(comp.loan_amount),
                "best_option_name": best_modality.name if best_modality else None,
                "term_months": best_modality.term_months if best_modality else None,
                "interest_rate": best_modality.interest_rate if best_modality else None,

                "modalities": [{
                    "name": m.name,
                    "monthly_payment": float(m.monthly_payment),
                    "total_amount": float(m.total_amount),
                    "type": m.type,
                    "term_months": m.term_months,       
                    "interest_rate": m.interest_rate    
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
            raise APIException("Comparação não encontrada.", 404)

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

        # Identifica a modalidade mais vantajosa (menor custo total) para destacar no PDF
        melhor_modalidade = None
        menor_total = float('inf')
        for m in comparacao.modalities:
            if float(m.total_amount) < menor_total:
                menor_total = float(m.total_amount)
                melhor_modalidade = m

        PAGE_WIDTH, PAGE_HEIGHT = letter
        MARGIN = 50
        BRAND_COLOR = colors.HexColor('#145c52')
        HIGHLIGHT_COLOR = colors.HexColor('#e8f5e9')
        HIGHLIGHT_BORDER = colors.HexColor('#2e7d32')
        BORDER_COLOR = colors.HexColor('#cccccc')
        TEXT_MUTED = colors.HexColor('#555555')

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setTitle(f"Relatório de Crédito #{comparison_id}")

        # Cabeçalho
        header_height = 80
        c.setFillColor(BRAND_COLOR)
        c.rect(0, PAGE_HEIGHT - header_height, PAGE_WIDTH, header_height, stroke=0, fill=1)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(MARGIN, PAGE_HEIGHT - 35, "Comparativo de Modalidades de Crédito")
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN, PAGE_HEIGHT - 55, f"CrediFab - Plataforma de Acesso a Crédito | Comparação #{comparison_id}")

        y_position = PAGE_HEIGHT - header_height - 30

        # Bloco de informações gerais
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y_position, "Informações da Simulação")
        y_position -= 18

        c.setFont("Helvetica", 10)
        c.setFillColor(TEXT_MUTED)
        empresa_nome = comparacao.company.name if comparacao.company else "N/A"
        usuario_nome = comparacao.user.name if comparacao.user else "N/A"

        info_rows = [
            ("Empresa:", empresa_nome, "Data da Simulação:", comparacao.created_at.strftime('%d/%m/%Y')),
            ("Solicitado por:", usuario_nome, "Valor Solicitado:", _fmt_currency(comparacao.loan_amount)),
        ]
        for esq_label, esq_valor, dir_label, dir_valor in info_rows:
            c.setFont("Helvetica-Bold", 9)
            c.drawString(MARGIN, y_position, esq_label)
            c.setFont("Helvetica", 9)
            c.drawString(MARGIN + 90, y_position, str(esq_valor))

            c.setFont("Helvetica-Bold", 9)
            c.drawString(320, y_position, dir_label)
            c.setFont("Helvetica", 9)
            c.drawString(320 + 100, y_position, str(dir_valor))
            y_position -= 16

        y_position -= 10
        c.setStrokeColor(BORDER_COLOR)
        c.line(MARGIN, y_position, PAGE_WIDTH - MARGIN, y_position)
        y_position -= 25

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(MARGIN, y_position, "Modalidades Comparadas")
        y_position -= 20

        box_width = PAGE_WIDTH - 2 * MARGIN
        box_height = 95
        box_gap = 15

        for m in comparacao.modalities:
            is_best = melhor_modalidade is not None and m.modality_id == melhor_modalidade.modality_id
            box_top = y_position
            box_bottom = box_top - box_height

            if is_best:
                c.setFillColor(HIGHLIGHT_COLOR)
                c.setStrokeColor(HIGHLIGHT_BORDER)
            else:
                c.setFillColor(colors.white)
                c.setStrokeColor(BORDER_COLOR)
            c.roundRect(MARGIN, box_bottom, box_width, box_height, 6, stroke=1, fill=1)

            inner_y = box_top - 20
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(MARGIN + 15, inner_y, f"{m.name} ({m.type.upper()})")

            if is_best:
                c.setFillColor(HIGHLIGHT_BORDER)
                c.setFont("Helvetica-Bold", 9)
                c.drawRightString(PAGE_WIDTH - MARGIN - 15, inner_y, "MELHOR OPÇÃO")

            if m.type.upper() == 'PF':
                inner_y -= 15
                c.setFillColor(colors.HexColor('#b26a00'))
                c.setFont("Helvetica-Oblique", 8)
                c.drawString(MARGIN + 15, inner_y, "Atenção: modalidade de crédito para Pessoa Física")

            c.setFillColor(colors.black)
            c.setFont("Helvetica", 10)
            inner_y -= 20
            c.drawString(MARGIN + 15, inner_y, f"Taxa de Juros: {m.interest_rate}% a.m.")
            c.drawString(MARGIN + 250, inner_y, f"Prazo: {m.term_months} meses")

            inner_y -= 18
            c.drawString(MARGIN + 15, inner_y, f"Valor da Parcela: {_fmt_currency(m.monthly_payment)}")

            inner_y -= 18
            c.drawString(
                MARGIN + 15, inner_y,
                f"Custo Total: {_fmt_currency(m.total_amount)}  (Juros: {_fmt_currency(m.total_interest)})"
            )

            y_position = box_bottom - box_gap

        # Rodapé
        c.setStrokeColor(BORDER_COLOR)
        c.line(MARGIN, 40, PAGE_WIDTH - MARGIN, 40)
        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(MARGIN, 28, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        c.drawRightString(PAGE_WIDTH - MARGIN, 28, "CrediFab - Contribuindo para o ODS 9.3")

        c.save()
        buffer.seek(0)
        return buffer, 200