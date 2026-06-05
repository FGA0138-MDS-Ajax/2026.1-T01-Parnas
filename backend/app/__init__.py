from flask import Flask
from app.config import Config, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa o banco de dados, as migrações e o JWT no app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Importação de TODOS os modelos para o Flask-Migrate registrar as tabelas
    from app.models.user import User
    from app.models.company import Company
    from app.models.user_company_association import user_company
    from app.models.category import Category
    from app.models.transaction import Transaction

    # Força a criação das tabelas automaticamente (essencial para o SQLite de teste)
    import os as _os
    migrations_path = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', 'migrations'))
    # Se não houver migrations, cria as tabelas (modo quickstart). Caso contrário, deixa Alembic gerenciar o schema.
    if not _os.path.exists(migrations_path):
        with app.app_context():
            db.create_all()

    # 1. Registro do Blueprint de autenticação (Login/Logout)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # 2. Centralização das rotas da API restrita com prefixo único (/api)
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')

    from app.routes.company_routes import company_bp
    app.register_blueprint(company_bp, url_prefix="/api/companies")

    from app.routes.category_routes import category_bp
    app.register_blueprint(category_bp, url_prefix="/api/categories")

    # Registro ÚNICO de transações (Removeu a duplicação antiga que causava erro)
    from app.routes.transaction_routes import transaction_bp
    app.register_blueprint(transaction_bp, url_prefix="/api/transactions")

    return app