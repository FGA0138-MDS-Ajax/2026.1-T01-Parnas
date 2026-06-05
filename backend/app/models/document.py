from app.config import db
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documento'
    
    id_documento = db.Column(db.Integer, primary_key=True)
    id_empresa = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    nome = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False) # Ex: 'fiscal', 'contabil', 'juridico'
    descricao = db.Column(db.Text)
    caminho_arquivo = db.Column(db.String(500), nullable=False)
    tamanho = db.Column(db.Integer) # Em bytes
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship('Company', backref='documentos')