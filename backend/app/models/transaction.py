from datetime import date
from app.config import db

class Transaction(db.Model):
    __tablename__ = 'transaction'
    
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    type = db.Column(db.String(20), nullable=False)
    
    # Foreign Keys com CASCADE 
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='CASCADE'), nullable=False)

    # Relacionamentos: usar strings evita importações circulares e deixa o código mais limpo
    company = db.relationship('Company', back_populates='transactions')
    user = db.relationship('User', back_populates='transactions')
    category = db.relationship('Category', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction {self.description} - {self.amount}>'