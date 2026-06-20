from datetime import date, datetime
from app.config import db

class Simulation(db.Model):
    __tablename__="simulation"

    simulation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_solicitado = db.Column(db.Numeric(10, 2), nullable=False)
    prazo_meses = db.Column(db.Integer, nullable=False)
    modalidade = db.Column(db.String(10), nullable=False)
    taxa_juros = db.Column(db.Numeric(5, 2), nullable=False)
    valor_parcela = db.Column(db.Numeric(10, 2), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    total_juros = db.Column(db.Numeric(10, 2), nullable=False)
    data_simulacao = db.Column(db.DateTime, default=date.today, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    
    empresa = db.relationship('Company', back_populates='simulations')
    usuario = db.relationship('User', back_populates='simulations')

    def __repr__(self):
        return f'<Simulation {self.modalidade} - {self.valor_solicitado}>'