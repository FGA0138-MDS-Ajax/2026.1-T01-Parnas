from datetime import date
from app.config import db

class Simulation(db.Model):
    __tablename__ = "simulation"

    simulation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loan_amount = db.Column(db.Numeric(10, 2), nullable=False)
    term_months = db.Column(db.Integer, nullable=False)
    modality = db.Column(db.String(10), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    monthly_payment = db.Column(db.Numeric(10, 2), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    total_interest = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=date.today, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    
    company = db.relationship('Company', back_populates='simulations')
    user = db.relationship('User', back_populates='simulations')
    
    def __repr__(self):
        return f'<Simulation {self.modality} - {self.loan_amount}>'