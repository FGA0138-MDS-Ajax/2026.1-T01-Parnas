from flask import Flask
from app.config import Config, db
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa o banco de dados e as migrações no app
    db.init_app(app)
    migrate.init_app(app, db)

    # Importação correta do modelo em inglês para o Flask-Migrate registrar a tabela
    from app.models.user import User

    return app