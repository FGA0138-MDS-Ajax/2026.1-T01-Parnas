from datetime import datetime
from app.config import db
from sqlalchemy import UniqueConstraint

class Category(db.Model):
    __tablename__ = 'category'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False) 
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Restrição: Não permitir o mesmo nome dentro da mesma empresa
    __table_args__ = (
        UniqueConstraint('name', 'company_id', name='_name_company_uc'),
    )

    company = db.relationship('Company', back_populates='categories')

    def __repr__(self):
        return f'<Category {self.name} - {self.type}>'