from app.config import db
from app.models.simulation import Simulation

class SimulationRepository:

    @staticmethod
    def get_by_id_and_company(simulation_id, company_id):
        return Simulation.query.filter_by(simulation_id=simulation_id,company_id=company_id).first()

    @staticmethod
    def list_by_company(company_id):
        """Lista todas as simulações vinculadas a uma empresa específica."""
        return Simulation.query.filter_by(company_id=company_id).all()

    @staticmethod
    def create(company_id, user_id, valor_solicitado, prazo_meses, modalidade, taxa_juros, valor_parcela, valor_total, total_juros):
        new_simulation = Simulation(
            company_id=company_id,
            user_id=user_id,
            valor_solicitado=valor_solicitado,
            prazo_meses=prazo_meses,
            modalidade=modalidade,
            taxa_juros=taxa_juros,
            valor_parcela=valor_parcela,
            valor_total=valor_total,
            total_juros=total_juros
        )
        db.session.add(new_simulation)
        db.session.commit()
        return new_simulation

    @staticmethod
    def delete(simulation):
        db.session.delete(simulation)
        db.session.commit()