from app.config import db
from app.models.payment import Payment

class PaymentRepository:
    @staticmethod
    def list_by_company(company_id):
        """Lista todas as formas de pagamento vinculadas a uma empresa específica."""
        return Payment.query.filter_by(company_id=company_id).all()


    @staticmethod
    def get_by_id_and_company(payment_id, company_id):
        """Busca uma forma de pagamento específica garantindo que pertence à empresa."""
        return Payment.query.filter_by(
            payment_id=payment_id, 
            company_id=company_id
        ).first()


    @staticmethod
    def create(name, company_id):
        """Cria uma nova forma de pagamento para a empresa."""
        new_payment = Payment(name=name, company_id=company_id)
        db.session.add(new_payment)
        db.session.commit()
        return new_payment


    @staticmethod
    def update(payment_id, company_id, new_name):
        """Edita o nome de uma forma de pagamento existente."""
        new_payment = PaymentRepository.get_by_id_and_company(payment_id, company_id)
        if new_payment:
            new_payment.name = new_name
            db.session.commit()
        return new_payment


    @staticmethod
    def delete(payment_id, company_id):
        """Exclui uma forma de pagamento da empresa."""
        new_payment = PaymentRepository.get_by_id_and_company(payment_id, company_id)
        if new_payment:
            db.session.delete(new_payment)
            db.session.commit()
            return True
        return False