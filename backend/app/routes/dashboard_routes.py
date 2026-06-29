from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.dashboard_schema import DashboardQuerySchema
from app.services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard_bp", __name__)
dashboard_schema = DashboardQuerySchema()

@dashboard_bp.route("", methods=["GET"])
@jwt_required()
def get_dashboard(company_id):
    user_id = int(get_jwt_identity())
    answer, status_code = DashboardService.build_dashboard(user_id, company_id)
    return jsonify(answer), status_code