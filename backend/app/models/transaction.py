from app.config import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False) # Representa a empresa/gestor
    type = db.Column(db.String(50), nullable=False) # 'receita' ou 'despesa'
    category = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # Índice em data e user_id para otimizar buscas
    __table_args__ = (
        db.Index('idx_transaction_date_user', 'date', 'user_id'),
    )
