from datetime import date
from app.config import db

class Document(db.Model):
    __tablename__ = 'document'
    
    document_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500), nullable=False)
    size = db.Column(db.Integer)
    created_at = db.Column(db.Date, default=date.today)

    # Relacionamentos
    company = db.relationship('Company', back_populates='documents')
    user = db.relationship('User', back_populates='documents')

    def __repr__(self):
        return f'<Document {self.name}>'