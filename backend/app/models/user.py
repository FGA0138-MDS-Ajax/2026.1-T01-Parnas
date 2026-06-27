from datetime import date
from app.config import db
from app.models.user_company_association import user_company

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False) 
    password_hash = db.Column(db.String(300), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    register_date = db.Column(db.Date, nullable=False, default=date.today)
    active_company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='SET NULL'), nullable=True)

    companies = db.relationship('Company', secondary=user_company, back_populates='users')
    active_company = db.relationship('Company', foreign_keys=[active_company_id])
    transactions = db.relationship('Transaction', back_populates='user')
    documents = db.relationship('Document', back_populates='user')
    simulations = db.relationship('Simulation', back_populates='user', cascade='all, delete-orphan')
    credit_comparisons = db.relationship('Comparison', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.name}>'    