from datetime import date
from app.config import db
from sqlalchemy import UniqueConstraint

class Payment(db.Model):
    __tablename__ = 'payment'
    
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=date.today)

    # Restrição: Não permitir o mesmo nome dentro da mesma empresa
    __table_args__ = (
        UniqueConstraint('name', 'company_id', name='_name_company_uc'),
    )

    company = db.relationship('Company', back_populates='payments')
    bills = db.relationship('Bill', back_populates='payment')
    transactions = db.relationship('Transaction', back_populates='payment', lazy=True)
    
    def __repr__(self):
        return f'<Payment {self.name}>'