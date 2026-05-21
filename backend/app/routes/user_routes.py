from flask import Blueprint, request, jsonify
from app.services.user_service import register_user

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    answer, status_code = register_user(data)
    return jsonify(answer), status_code