from flask import Flask
from flask_cors import CORS
from app.config import Config, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from app.exceptions.api_exception import APIException

migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    frontend_origin = app.config['FRONTEND_URL'].rstrip('/')
    CORS(app, origins=[frontend_origin], supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # --- NOVO BLOCO: Middleware para checar se o usuário está ativo ---
    @jwt.token_in_blocklist_loader
    def check_if_user_is_inactive(jwt_header, jwt_payload):
        from app.models.user import User
        user_id = jwt_payload.get("sub")

        if not user_id:
            return False

        user = db.session.query(User).filter(User.user_id == user_id).first()

        if not user or not user.is_active:
            return True

        return False

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {"erro": "Conta não encontrada ou desativada"}, 401

    # Importação de TODOS os modelos para o Flask-Migrate registrar as tabelas
    from app.models.user import User
    from app.models.company import Company
    from app.models.user_company_association import user_company
    from app.models.category import Category
    from app.models.payment import Payment
    from app.models.transaction import Transaction
    from app.models.bill import Bill
    from app.models.document import Document
    from app.models.simulation import Simulation
    from app.models.comparison import Comparison, ComparisonModality
    
    @app.errorhandler(APIException)
    def handle_api_error(error):
        return {"erro": error.message}, error.status_code

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')

    from app.routes.company_routes import company_bp
    app.register_blueprint(company_bp, url_prefix="/api/companies")

    from app.routes.category_routes import category_bp
    app.register_blueprint(category_bp, url_prefix='/api/companies/<int:company_id>/categories')

    from app.routes.payment_routes import payment_bp
    app.register_blueprint(payment_bp, url_prefix='/api/companies/<int:company_id>/payments')

    from app.routes.transaction_routes import transaction_bp
    app.register_blueprint(transaction_bp, url_prefix="/api/companies/<int:company_id>/transactions")

    from app.routes.bill_routes import bill_bp
    app.register_blueprint(bill_bp, url_prefix='/api/companies/<int:company_id>/bills')

    from app.routes.document_routes import document_bp
    app.register_blueprint(document_bp, url_prefix='/api/companies/<int:company_id>/documents')

    from app.routes.simulation_routes import simulation_bp
    app.register_blueprint(simulation_bp, url_prefix='/api/companies/<int:company_id>/simulations')

    from app.routes.comparison_routes import comparison_bp
    app.register_blueprint(comparison_bp, url_prefix='/api/companies/<int:company_id>/comparisons')

    from app.routes.report_routes import report_bp
    app.register_blueprint(report_bp, url_prefix='/api/companies/<int:company_id>/reports')

    # Registra o Blueprint do Dashboard Financeiro
    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/api/companies/<int:company_id>/dashboard')
    # Registra o Blueprint de sessões e empresas
    from app.routes.session_routes import session_bp
    app.register_blueprint(session_bp, url_prefix='/api')

    return app