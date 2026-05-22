from datetime import datetime
from app.config import db

class UserCompany(db.Model):
    __tablename__ = 'user_company'
    
    user_company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    role = db.Column(db.String(50), default='admin', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship('User', backref=db.backref('companies', lazy=True))
    company = db.relationship('Company', backref=db.backref('users', lazy=True))
    
    def __repr__(self):
        return f'<UserCompany user_id={self.user_id} company_id={self.company_id}>'