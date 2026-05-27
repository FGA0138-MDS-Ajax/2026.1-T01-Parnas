from datetime import date
from app.config import db
from app.models.user_company_association import user_company

class Company(db.Model):
    __tablename__ = 'company'

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    register_date = db.Column(db.Date, nullable=False, default=date.today)
    
    users = db.relationship('User', secondary=user_company, back_populates='companies')
    transactions = db.relationship('Transaction', back_populates='company')

    def __repr__(self):
        return f'<Company {self.name}>'