from app.repositories.payment_repository import PaymentRepository
from app.repositories.company_repository import CompanyRepository
from app.exceptions.api_exception import APIException

class PaymentService:
    @staticmethod
    def add_payment(user_id, company_id, data):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
        
        try:
            new_payment = PaymentRepository.create(
                name=data.get("name"),
                company_id=company_id
            )
            return {"payment": new_payment}, 201
        except Exception as e:
            return {"erro": f"Erro interno ao salvar a forma de pagamento: {str(e)}"}, 500


    @staticmethod
    def get_payments(user_id, company_id):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

        payments = PaymentRepository.list_by_company(company_id)
        return {"payments": payments}, 200


    @staticmethod
    def update_payment(user_id, company_id, payment_id, data):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

        payment = PaymentRepository.get_by_id_and_company(payment_id, company_id)
        if not payment:
            raise APIException("Forma de pagamento não encontrada para esta empresa.", 404)

        # update() sobrescreve sempre, então preenche com o valor atual se não vier no data
        new_name = data.get("name", payment.name)

        try:
            updated = PaymentRepository.update(payment_id, company_id, new_name)
            return {"payment": updated}, 200
        except Exception as e:
            return {"erro": f"Erro interno ao atualizar: {str(e)}"}, 500


    @staticmethod
    def delete_payment(user_id, company_id, payment_id):
        try:
            company = CompanyRepository.get_by_id(company_id)
            if not company:
                raise APIException("Empresa não encontrada.", 404)
            
            access = CompanyRepository.check_user_access(company_id, user_id)
            if not access:
                raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

            success = PaymentRepository.delete(payment_id, company_id)
            if not success:
                raise APIException("Forma de pagamento não encontrada para esta empresa.", 404)
            
            return {"msg": "Forma de pagamento deletada com sucesso!"}, 200
        
        except APIException as ve:
            raise ve
        except Exception as e:
            return {"erro": f"Erro interno ao deletar: {str(e)}"}, 500