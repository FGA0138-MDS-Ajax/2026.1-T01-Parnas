from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.report_service import generate_report
from app.schemas.report_schema import RelatorioQuerySchema
from marshmallow import ValidationError

report_bp = Blueprint("report_bp", __name__)

relatorio_schema = RelatorioQuerySchema()

@report_bp.route("/", methods=["GET"])
@jwt_required()
def get_relatorio():
    user_id = int(get_jwt_identity())
    try:
        data = relatorio_schema.load(request.args)
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400
    
    answer, status_code = generate_report(user_id, data)
    
    return jsonify(answer), status_code