import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'uma-chave-secreta-muito-segura')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres@localhost:5432/parnas_db'
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False