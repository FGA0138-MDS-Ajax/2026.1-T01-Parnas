from datetime import date
from app.config import db

class Account(db.Model):
    __tablename__ = 'account'
    
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='CASCADE'), nullable=False)
    
    description = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Numeric(12, 2), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'receita' ou 'despesa'
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pendente') # 'pendente', 'quitado'
    payment_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.Date, default=date.today)

    # Relacionamentos
    company = db.relationship('Company', back_populates='accounts')
    category = db.relationship('Category', backref='accounts')
    transactions = db.relationship('Transaction', back_populates='account')

    def __repr__(self):
        return f'<Account {self.description} - {self.value}>'