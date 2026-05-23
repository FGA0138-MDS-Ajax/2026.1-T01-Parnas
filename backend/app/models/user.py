from datetime import datetime
from app.config import db
from app.models.user_company_association import user_company

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False) 
    password_hash = db.Column(db.String(300), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    register_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    companies = db.relationship('Company', secondary=user_company, back_populates='users')

    def __repr__(self):
        return f'<User {self.name}>'    