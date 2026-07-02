from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.schemas.simulation_schema import SimulationCalculateDTO, SimulationSaveDTO
from app.services.simulation_service import SimulationService

simulation_bp = Blueprint("simulation_bp", __name__)
calc_schema = SimulationCalculateDTO()
save_schema = SimulationSaveDTO()


@simulation_bp.route("/calculate", methods=["POST"])
@jwt_required()
def calculate(company_id):
    user_id = int(get_jwt_identity())
    try:
        data = calc_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400
    #corrige o nome da função no service que é process_simulation
    answer = SimulationService.process_simulation(user_id, company_id, data)
    return jsonify(answer), 200


@simulation_bp.route("/", methods=["POST"])
@jwt_required()
def create(company_id):
    try:
        data = save_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"erros_de_validacao": err.messages}), 400
    current_user_id = int(get_jwt_identity())
    answer, status_code = SimulationService.save_simulation(current_user_id, company_id, data)
    return jsonify(answer), status_code


@simulation_bp.route("/", methods=["GET"])
@jwt_required()
def get_all(company_id):
    current_user_id = int(get_jwt_identity())
    #corrige para o nome da função no service que é get_simulation (singular)
    answer, status_code = SimulationService.get_simulation(current_user_id, company_id)
    return jsonify(answer), status_code


@simulation_bp.route("/<int:simulation_id>", methods=["DELETE"])
@jwt_required()
def delete(company_id, simulation_id):
    current_user_id = int(get_jwt_identity())
    answer, status_code = SimulationService.delete_simulation(current_user_id, company_id, simulation_id)
    return jsonify(answer), status_code