from datetime import datetime
from app.config import db

class Simulation(db.Model):
    __tablename__ = 'simulation'

    id_simulacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_empresa = db.Column(
        db.Integer,
        db.ForeignKey('company.company_id', ondelete='CASCADE'),
        nullable=False
    )
    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False
    )
    valor_solicitado = db.Column(db.Numeric(14, 2), nullable=False)
    prazo_meses = db.Column(db.Integer, nullable=False)
    modalidade = db.Column(db.String(10), nullable=False)
    taxa_juros = db.Column(db.Numeric(8, 4), nullable=False)
    valor_parcela = db.Column(db.Numeric(14, 2), nullable=False)
    valor_total = db.Column(db.Numeric(14, 2), nullable=False)
    total_juros = db.Column(db.Numeric(14, 2), nullable=False)
    data_simulacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    company = db.relationship('Company', back_populates='simulations')
    user = db.relationship('User', back_populates='simulations')

    def __repr__(self):
        return f'<Simulation {self.id_simulacao} - {self.modalidade}>'
