from app.models.bill import Bill
from app.models.transaction import Transaction
from app.config import db
from datetime import date, datetime
from flask_jwt_extended import get_jwt


class BillService:

    @staticmethod
    def _get_company_id():
        claims = get_jwt()
        return claims.get("active_company_id")

    @staticmethod
    def create_bill(data):
        company_id = BillService._get_company_id()
        if not company_id:
            return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

        nova_conta = Bill(
            description=data['description'],
            amount=data['amount'],
            type=data['type'],  # 'pagar' ou 'receber'
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date(),
            category_id=data['category_id'],
            company_id=company_id
        )

        db.session.add(nova_conta)
        db.session.commit()
        return {"mensagem": "Conta criada com sucesso!", "id": nova_conta.bill_id}, 201

    @staticmethod
    def get_bills(status=None):
        company_id = BillService._get_company_id()
        if not company_id:
            return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

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
            "payment_date": c.payment_date.isoformat() if c.payment_date else None
        } for c in contas]

        return resultado, 200

    @staticmethod
    def update_bill(bill_id, data):
        company_id = BillService._get_company_id()
        if not company_id:
            return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400
        conta = Bill.query.filter_by(bill_id=bill_id, company_id=company_id).first()

        if not conta:
            return {"erro": "Conta não encontrada"}, 404

        # Regra de negócio: Bloquear edição de conta quitada
        if conta.status == 'quitado':
            return {"erro": "Não é possível editar uma conta que já foi quitada."}, 400

        conta.description = data.get('description', conta.description)
        conta.amount = data.get('amount', conta.amount)
        if 'due_date' in data:
            conta.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()

        db.session.commit()
        return {"mensagem": "Conta atualizada com sucesso!"}, 200

    @staticmethod
    def delete_bill(bill_id):
        company_id = BillService._get_company_id()
        if not company_id:
            return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400
        conta = Bill.query.filter_by(bill_id=bill_id, company_id=company_id).first()

        if not conta:
            return {"erro": "Conta não encontrada"}, 404

        # Regra de negócio: Bloquear exclusão de conta quitada
        if conta.status == 'quitado':
            return {"erro": "Não é possível excluir uma conta que já foi quitada."}, 400

        db.session.delete(conta)
        db.session.commit()
        return {"mensagem": "Conta excluída com sucesso!"}, 200

    @staticmethod
    def pay_bill(user_id, bill_id):
        company_id = BillService._get_company_id()
        if not company_id:
            return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400
        conta = Bill.query.filter_by(bill_id=bill_id, company_id=company_id).first()

        if not conta:
            return {"erro": "Conta não encontrada"}, 404

        if conta.status == 'quitado':
            return {"erro": "Esta conta já está quitada."}, 400

        # 1. Atualiza a conta para quitada
        conta.status = 'quitado'
        conta.payment_date = date.today()

        # 2. Regra de negócio: Gera a transação automaticamente
        transaction_type = 'receita' if conta.type.lower() == 'receber' else 'despesa'

        nova_transacao = Transaction(
            description=f"Quitação: {conta.description}",
            amount=conta.amount,
            date=conta.payment_date,
            type=transaction_type,
            company_id=company_id,
            user_id=user_id,
            category_id=conta.category_id,
            bill_id=conta.bill_id
        )

        db.session.add(nova_transacao)
        db.session.commit()

        return {"mensagem": "Conta quitada e transação gerada com sucesso!"}, 200