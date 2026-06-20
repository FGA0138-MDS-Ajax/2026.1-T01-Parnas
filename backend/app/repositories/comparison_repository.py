from app.config import db
from app.models.comparison import Comparison, ComparisonModality

class ComparisonRepository:
    
    @staticmethod
    def list_by_company(company_id):
        # Retorna comparações de uma empresa
        return Comparison.query.filter_by(company_id=company_id).all()

    @staticmethod
    def get_details(comparison_id, company_id):
        # Necessário para exportar PDF e exibir o "lado a lado"
        # O backend usará isso para destacar a modalidade mais vantajosa
        return Comparison.query.filter_by(
            comparison_id=comparison_id, 
            company_id=company_id
        ).first()
        
    @staticmethod
    def save(comparison_data, modalities_list):
        # AVISO: Dependência da US13 para o cálculo dos campos
        # Validação de limite: o controller deve garantir len(modalities_list) <= 4
        new_comparison = Comparison(**comparison_data)
        db.session.add(new_comparison)
        db.session.flush()

        for mod in modalities_list:
            new_modality = ComparisonModality(comparison_id=new_comparison.comparison_id, **mod)
            db.session.add(new_modality)
            
        db.session.commit()
        return new_comparison