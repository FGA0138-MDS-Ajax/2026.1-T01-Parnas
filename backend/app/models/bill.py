from datetime import date, datetime
from app.config import db

class Bill(db.Model):
    __tablename__ = 'bill'

    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    # tipo:'pagar' ou 'receber' | status: 'pendente' ou 'quitado'
    type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='pendente')
    due_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys com CASCADE e RESTRICT seguindo a lógica de negócio
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='RESTRICT'), nullable=False)
    company = db.relationship('Company', backref='bills')
    category = db.relationship('Category', backref='bills')

    # Relacionamento reverso com as transações geradas por esta conta
    transactions = db.relationship('Transaction', back_populates='bill', lazy=True)

    def __repr__(self):
        return f'<Bill {self.description} - {self.type} - R$ {self.amount} ({self.status})>'