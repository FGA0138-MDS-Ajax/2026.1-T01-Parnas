from datetime import date
from app.config import db

class Comparison(db.Model):
    __tablename__ = 'comparison'
    
    comparison_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=date.today)

    # Relacionamento simples (o Comparison pertence a UMA empresa e FOI CRIADO POR UM usuário)
    company = db.relationship('Company', back_populates='comparisons')
    user = db.relationship('User', back_populates='comparisons')
    modalities = db.relationship('ComparisonModality', back_populates='comparison', cascade='all, delete-orphan')

class ComparisonModality(db.Model):
    __tablename__ = 'comparison_modality'
    
    modality_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comparison_id = db.Column(db.Integer, db.ForeignKey('comparison.comparison_id', ondelete='CASCADE'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    term_months = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'PF' ou 'PJ'
    
    # Resultados calculados (Requisito: exibir parcela, total pago e juros)
    monthly_payment = db.Column(db.Numeric(10, 2), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    total_interest = db.Column(db.Numeric(10, 2), nullable=False)

    comparison = db.relationship('Comparison', back_populates='modalities')