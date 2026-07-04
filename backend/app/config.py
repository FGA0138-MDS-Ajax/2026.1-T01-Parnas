import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'uma-chave-secreta-muito-segura')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'chave-super-secreta-do-jwt')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # Se existir a variável DATABASE_URL (no .env ou na Render), usa ela.
    # Caso contrário, usa o SQLite local para não travar o sistema.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024 # 50MB
    ALLOWED_EXTENSIONS = {'pdf','txt','md'}
    ALLOWED_DOCUMENT_TYPES = ['fiscal', 'contabil', 'juridico']

    # --- CONFIGURAÇÕES DO FLASK-MAIL ---
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # --- CONFIGURAÇÃO DO FRONTEND URL ---
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')