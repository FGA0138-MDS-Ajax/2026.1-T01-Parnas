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

    # Importação do modelo para o Flask-Migrate registrar a tabela
    from app.models.user import User

    # Força a criação das tabelas automaticamente (essencial para o SQLite de teste)
    with app.app_context():
        db.create_all()

    # Registra o Blueprint de autenticação (Login/Logout)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Centralização da ativação dos módulos de rotas de usuários
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')  # Mudei para /api para não dar conflito de rota com /auth

    return app