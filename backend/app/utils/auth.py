from flask_jwt_extended import jwt_required, get_jwt_identity


# Este arquivo centraliza o middleware de autenticação para rotas protegidas.
# Qualquer rota futura do CREDIFAB precisará apenas importar e usar o decorador @jwt_required()

def exemplo_rota_protegida():
    """
    Exemplo prático de como a equipe de desenvolvimento usará isso nas outras branches:

    from app.utils.auth import jwt_required, get_jwt_identity

    @app.route('/dashboard')
    @jwt_required()
    def dashboard():
        # Captura o ID do usuário que estava guardado dentro do Token JWT
        usuario_logado_id = get_jwt_identity()
        return {"mensagem": f"Bem-vindo à área protegida, usuário {usuario_logado_id}"}
    """
    pass