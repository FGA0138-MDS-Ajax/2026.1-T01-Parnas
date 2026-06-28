from app.models.simulation import Simulation
from app.repositories.base_repository import BaseRepository


class SimulationRepository(BaseRepository):
    
    _base = BaseRepository(Simulation)
    
    @staticmethod
    def get_by_id_and_company(simulation_id, company_id):
        return Simulation.query.filter_by(simulation_id=simulation_id, company_id=company_id).first()
    
    @staticmethod
    def list_by_company(company_id):
        return Simulation.query.filter_by(company_id=company_id).all()
    
    @staticmethod
    def create(company_id, user_id, loan_amount, term_months, modality, interest_rate, monthly_payment, total_amount, total_interest):
        new_simulation = Simulation(
            company_id=company_id,
            user_id=user_id,
            loan_amount=loan_amount,
            term_months=term_months,
            modality=modality,
            interest_rate=interest_rate,
            monthly_payment=monthly_payment,
            total_amount=total_amount,
            total_interest=total_interest
        )
        return SimulationRepository._base.save(new_simulation)
    
    @staticmethod
    def delete(simulation):
        SimulationRepository._base.delete(simulation)