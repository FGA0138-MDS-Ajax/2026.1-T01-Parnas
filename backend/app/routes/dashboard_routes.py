from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.schemas.dashboard_schema import DashboardQuerySchema
from app.services.dashboard_service import build_dashboard

dashboard_bp = Blueprint("dashboard_bp", __name__)
dashboard_schema = DashboardQuerySchema()

@dashboard_bp.route("", methods=["GET"])
@jwt_required()
def get_dashboard(company_id):

    answer, status_code = build_dashboard(company_id)
    return jsonify(answer), status_code