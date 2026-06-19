from app.models.user import User
from flask_jwt_extended import create_access_token


class SessionService:

    @staticmethod
    def get_user_companies(user_id):
        """Retorna todas as empresas vinculadas ao usuário logado"""
        user = User.query.get(user_id)
        if not user:
            return {"erro": "Usuário não encontrado"}, 404

        companies_data = []
        for company in user.companies:
            companies_data.append({
                "company_id": company.company_id,
                "name": company.name,  # Ou o nome do campo que sua equipe usa para Razão Social/Fantasia
                "cnpj": company.cnpj
            })

        return companies_data, 200

    @staticmethod
    def set_active_company(user_id, company_id):
        """Verifica se o usuário pertence à empresa e gera um novo token com a empresa ativa"""
        user = User.query.get(user_id)

        # Verifica se o company_id solicitado realmente está na lista de empresas do usuário
        company_exists = any(c.company_id == company_id for c in user.companies)

        if not company_exists:
            return {"erro": "Você não tem permissão para acessar esta empresa"}, 403

        # Cria um NOVO token JWT, injetando o active_company_id dentro do Payload dele
        # Assim, todas as requisições futuras saberão de qual empresa estamos falando
        additional_claims = {"active_company_id": company_id}
        new_access_token = create_access_token(
            identity=user_id,
            additional_claims=additional_claims
        )

        return {
            "mensagem": "Empresa ativa definida com sucesso",
            "token": new_access_token,
            "active_company_id": company_id
        }, 200