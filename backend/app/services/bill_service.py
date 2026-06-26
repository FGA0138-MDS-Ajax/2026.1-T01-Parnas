from app.models.bill import Bill
from app.models.transaction import Transaction
from app.models.user import User
from app.config import db
from datetime import date, datetime

class BillService:

    @staticmethod
    def _validate_user_company_access(user_id, company_id):
        """Verifica se o usuário tem permissão para a empresa informada"""
        user = db.session.query(User).filter(User.user_id == user_id).first()
        user_companies_ids = [c.company_id for c in user.companies] if user else []
        return company_id in user_companies_ids

    @staticmethod
    def create_bill(user_id, data):
        company_id = data['company_id']
        
        if not BillService._validate_user_company_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        nova_conta = Bill(
            description=data['description'],
            amount=data['amount'],
            type=data['type'],
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date(),
            category_id=data['category_id'],
            company_id=company_id
        )

        db.session.add(nova_conta)
        db.session.commit()
        return {"mensagem": "Conta criada com sucesso!", "id": nova_conta.bill_id}, 201

    @staticmethod
    def get_bills(user_id, company_id, status=None):
        if not BillService._validate_user_company_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        query = Bill.query.filter_by(company_id=company_id)
        if status:
            query = query.filter_by(status=status)

        contas = query.order_by(Bill.due_date.asc()).all()

        resultado = [{
            "id": c.bill_id,
            "description": c.description,
            "amount": float(c.amount),
            "type": c.type,
            "status": c.status,
            "due_date": c.due_date.isoformat(),
            "payment_date": c.payment_date.isoformat() if c.payment_date else None,
            "category_id": c.category_id
        } for c in contas]

        return resultado, 200

    @staticmethod
    def update_bill(user_id, company_id, bill_id, data):
        if not BillService._validate_user_company_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        conta = Bill.query.filter_by(bill_id=bill_id, company_id=company_id).first()

        if not conta:
            return {"erro": "Conta não encontrada"}, 404

        if conta.status == 'quitado':
            return {"erro": "Não é possível editar uma conta que já foi quitada."}, 400

        conta.description = data.get('description', conta.description)
        conta.amount = data.get('amount', conta.amount)
        if 'due_date' in data:
            conta.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        if 'category_id' in data:
            conta.category_id = data['category_id']

        db.session.commit()
        return {"mensagem": "Conta atualizada com sucesso!"}, 200

    @staticmethod
    def delete_bill(user_id, company_id, bill_id):
        if not BillService._validate_user_company_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        conta = Bill.query.filter_by(bill_id=bill_id, company_id=company_id).first()

        if not conta:
            return {"erro": "Conta não encontrada"}, 404

        if conta.status == 'quitado':
            return {"erro": "Não é possível excluir uma conta que já foi quitada."}, 400

        db.session.delete(conta)
        db.session.commit()
        return {"mensagem": "Conta excluída com sucesso!"}, 200

    @staticmethod
    def pay_bill(user_id, company_id, bill_id):
        if not BillService._validate_user_company_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        conta = Bill.query.filter_by(bill_id=bill_id, company_id=company_id).first()

        if not conta:
            return {"erro": "Conta não encontrada"}, 404

        if conta.status == 'quitado':
            return {"erro": "Esta conta já está quitada."}, 400

        # atualiza a conta para quitada
        conta.status = 'quitado'
        conta.payment_date = date.today()

        # gera a transação apontando o TIPO corretamente 
        nova_transacao = Transaction(
            description=f"Quitação: {conta.description}",
            amount=conta.amount,
            date=conta.payment_date,
            company_id=company_id,
            user_id=user_id,
            category_id=conta.category_id,
            bill_id=conta.bill_id,
            type='despesa' if conta.type == 'pagar' else 'receita'
        )

        db.session.add(nova_transacao)
        db.session.commit()

        return {"mensagem": "Conta quitada e transação gerada com sucesso!"}, 200