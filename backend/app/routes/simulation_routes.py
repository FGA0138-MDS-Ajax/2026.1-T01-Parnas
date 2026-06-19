from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.schemas.simulation_schema import SimulationCalculateDTO, SimulationSaveDTO
from app.services.simulation_service import (
    process_simulation,
    save_simulation,
    get_simulation,
    delete_simulation
)

simulation_bp = Blueprint("simulation_bp", __name__)

calc_schema = SimulationCalculateDTO()
save_schema = SimulationSaveDTO()

@simulation_bp.route("/calculate", methods=["POST"])
@jwt_required()
def calculate():
    try:
        data = calc_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    answer = process_simulation(data)
    return jsonify(answer), 200

@simulation_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    try:
        data = save_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400

    current_user = get_jwt_identity()
    answer, status_code = save_simulation(data, current_user)
    return jsonify(answer), status_code

@simulation_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    answer, status_code = get_simulation()
    return jsonify(answer), status_code


@simulation_bp.route("/<int:simulation_id>", methods=["DELETE"])
@jwt_required()
def delete(simulation_id):
    answer, status_code = delete_simulation(simulation_id)
    return jsonify(answer), status_code