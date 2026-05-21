from datetime import datetime
from app.config import db

class User(db.Model):

    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(150),unique=True,nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False) 
    password_hash = db.Column(db.String(300),nullable=False)
    birth_date = db.Column(db.Date,nullable=False)
    register_date = db.Column(db.Date,nullable=False)

    #TO DO: Apos criarmos a tabela de empresa, fazer o relacionamento N:N entre elas 

    def __repr__(self):
        return super().__repr__()