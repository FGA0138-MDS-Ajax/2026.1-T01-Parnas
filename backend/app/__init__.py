from flask import Flask # Removido o 'app' daqui
from app.config import Config, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.exceptions.api_exception import APIException

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa o banco de dados, as migrações e o JWT no app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # --- NOVO BLOCO: Middleware para checar se o usuário está ativo ---
    @jwt.token_in_blocklist_loader
    def check_if_user_is_inactive(jwt_header, jwt_payload):
        from app.models.user import User
        # O "sub" é onde o JWT guarda a identidade (o user_id)
        user_id = jwt_payload.get("sub")

        if not user_id:
            return False

        # Busca o usuário no banco de dados
        user = db.session.query(User).filter(User.user_id == user_id).first()

        # Se o usuário não existir OU estiver desativado (soft delete), bloqueia!
        if not user or not user.is_active:
            return True  # True significa "Sim, o token deve ser bloqueado"

        return False

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        # Essa é a resposta que o Frontend vai receber quando cair no bloqueio acima
        return {"erro": "Conta não encontrada ou desativada"}, 401

    # Importação de TODOS os modelos para o Flask-Migrate registrar as tabelas
    from app.models.user import User
    from app.models.company import Company
    from app.models.user_company_association import user_company
    from app.models.category import Category
    from app.models.transaction import Transaction
    from app.models.bill import Bill
    from app.models.document import Document
    from app.models.simulation import Simulation
    from app.models.comparison import Comparison, ComparisonModality

    with app.app_context():
        db.create_all()

    @app.errorhandler(APIException)
    def handle_api_error(error):
        return {"erro": error.message}, error.status_code
    
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

    # Registra o Blueprint de contas a pagar/receber
    from app.routes.bill_routes import bill_bp
    app.register_blueprint(bill_bp, url_prefix='/api/contas')

    # Registra o Blueprint de documentos (centralização documental)
    from app.routes.document_routes import document_bp
    app.register_blueprint(document_bp, url_prefix='/api/documentos')

    # Registra o Blueprint de simulação de crédito
    from app.routes.simulation_routes import simulation_bp
    app.register_blueprint(simulation_bp, url_prefix='/api/simulations')

    # Registra o Blueprint de comparação de modalidades de crédito
    from app.routes.comparison_routes import comparison_bp
    app.register_blueprint(comparison_bp, url_prefix='/api/comparacoes')
    
    # Registra o Blueprint de relatórios financeiros
    from app.routes.report_routes import report_bp
    app.register_blueprint(report_bp, url_prefix='/api/reports')

    # Registra o Blueprint de sessões e empresas
    from app.routes.session_routes import session_bp
    app.register_blueprint(session_bp, url_prefix='/api')

    return app