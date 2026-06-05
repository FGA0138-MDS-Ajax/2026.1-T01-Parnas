from app.config import db
from app.models.simulation import Simulation


class SimulationRepository:

    @staticmethod
    def list_by_company(company_id):
        return (
            Simulation.query
            .filter_by(id_empresa=company_id)
            .order_by(Simulation.data_simulacao.desc())
            .all()
        )

    @staticmethod
    def get_by_id_and_company(simulation_id, company_id):
        return Simulation.query.filter_by(
            id_simulacao=simulation_id,
            id_empresa=company_id
        ).first()

    @staticmethod
    def create(**data):
        simulation = Simulation(**data)
        db.session.add(simulation)
        db.session.commit()
        return simulation

    @staticmethod
    def delete(simulation_id, company_id):
        simulation = SimulationRepository.get_by_id_and_company(simulation_id, company_id)
        if not simulation:
            return False

        db.session.delete(simulation)
        db.session.commit()
        return True
