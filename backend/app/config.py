import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'uma-chave-secreta-muito-segura')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'chave-super-secreta-do-jwt')

    # Se existir a variável DATABASE_URL (no .env ou na Render), usa ela.
    # Caso contrário, usa o SQLite local para não travar o sistema.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False