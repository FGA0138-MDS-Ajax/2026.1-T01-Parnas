from app.config import db
from app.models.comparison import Comparison, ComparisonModality
from app.repositories.base_repository import BaseRepository


class ComparisonRepository(BaseRepository):
    
    _base = BaseRepository(Comparison)
    
    @staticmethod
    def list_by_company(company_id):
        return Comparison.query.filter_by(company_id=company_id).all()
    
    @staticmethod
    def get_details(comparison_id, company_id):
        return Comparison.query.filter_by(
            comparison_id=comparison_id, 
            company_id=company_id
        ).first()
    
    @staticmethod
    def save(comparison_data, modalities_list):
        new_comparison = Comparison(**comparison_data)
        ComparisonRepository._base.save(new_comparison)
        
        for mod in modalities_list:
            new_modality = ComparisonModality(comparison_id=new_comparison.comparison_id, **mod)
            db.session.add(new_modality)
        
        db.session.commit()
        return new_comparison