from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.comparison_service import ComparisonService

comparison_bp = Blueprint('comparisons', __name__)


@comparison_bp.route('/calcular', methods=['POST'])
@jwt_required()
def calculate(company_id):
    """Apenas calcula e devolve o resultado para a tela (não salva)"""
    user_id = get_jwt_identity()
    data = request.get_json()
    resultado, status_code = ComparisonService.calculate_simulation(user_id, company_id, data)
    return jsonify(resultado), status_code


@comparison_bp.route('/', methods=['POST'])
@jwt_required()
def save_comparison(company_id):
    """Calcula e salva no banco de dados"""
    user_id = get_jwt_identity()
    data = request.get_json()
    resultado, status_code = ComparisonService.save_comparison(user_id, company_id, data)
    return jsonify(resultado), status_code


@comparison_bp.route('/', methods=['GET'])
@jwt_required()
def get_comparisons(company_id):
    """Lista o histórico de comparações da empresa"""
    user_id = get_jwt_identity()
    resultado, status_code = ComparisonService.get_comparisons(user_id, company_id)
    return jsonify(resultado), status_code


@comparison_bp.route('/<int:comparison_id>', methods=['DELETE'])
@jwt_required()
def delete_comparison(company_id, comparison_id):
    """Exclui uma comparação do histórico"""
    user_id = get_jwt_identity()
    resultado, status_code = ComparisonService.delete_comparison(user_id, company_id, comparison_id)
    return jsonify(resultado), status_code


@comparison_bp.route('/<int:comparison_id>/exportar', methods=['GET'])
@jwt_required()
def export_pdf(company_id, comparison_id):
    """Gera e faz o download do PDF da comparação"""
    user_id = get_jwt_identity()
    buffer, status_code = ComparisonService.generate_pdf_report(user_id, company_id, comparison_id)

    # Se retornou erro, devolve o JSON de erro
    if status_code != 200:
        return jsonify(buffer), status_code

    # Se deu tudo certo, envia o buffer como um arquivo PDF
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"comparativo_credito_{comparison_id}.pdf",
        mimetype='application/pdf'
    )