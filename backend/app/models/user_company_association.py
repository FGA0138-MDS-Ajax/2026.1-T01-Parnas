from app.config import db

user_company = db.Table('user_company',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True),
    db.Column('company_id', db.Integer, db.ForeignKey('company.company_id', ondelete='CASCADE'), primary_key=True)
)