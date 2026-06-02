from app.config import db

user_company = db.Table('user_company',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('company_id', db.Integer, db.ForeignKey('company.company_id'), primary_key=True)
)