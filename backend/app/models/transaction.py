from datetime import date, datetime
from app.config import db

class Transaction(db.Model):
    __tablename__ = 'transaction'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='SET NULL'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='RESTRICT'), nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.bill_id', ondelete='SET NULL'), nullable=True)

    # Relacionamentos 
    company = db.relationship('Company', back_populates='transactions')
    user = db.relationship('User', back_populates='transactions')
    category = db.relationship('Category', back_populates='transactions')
    bill = db.relationship('Bill', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction {self.description} - {self.amount}>'