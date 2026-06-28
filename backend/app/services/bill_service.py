from datetime import date, datetime
from app.repositories.bill_repository import BillRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository

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

    try:
        nova_conta = BillRepository.create(
            company_id=company_id,
            description=data['description'],
            amount=data['amount'],
            type=data['type'],
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date(),
            category_id=data['category_id']
        )
        return {"mensagem": "Conta criada com sucesso!", "id": nova_conta.bill_id}, 201
    except Exception as e:
        return {"erro": "Ocorreu um erro interno ao criar a conta."}, 500

    @staticmethod
    def get_bills(user_id, company_id, status=None):
        if not BillService._validate_user_company_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

def get_bills(user_id, status=None):
    company_id = _get_company_id(user_id)
    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400
    contas = BillRepository.list_by_company(company_id, status=status)

    resultado = [{
        "id": c.bill_id,
        "description": c.description,
        "amount": float(c.amount),
        "type": c.type,
        "status": c.status,
        "due_date": c.due_date.isoformat(),
        "payment_date": c.payment_date.isoformat() if c.payment_date else None
    } for c in contas]

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

    try:
        BillRepository.save(conta)
        return {"mensagem": "Conta atualizada com sucesso!"}, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro interno ao atualizar a conta."}, 500


    @staticmethod
    def delete_bill(user_id, company_id, bill_id):
        if not BillService._validate_user_company_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        conta = Bill.query.filter_by(bill_id=bill_id, company_id=company_id).first()

    if not conta:
        return {"erro": "Conta não encontrada"}, 404

        if conta.status == 'quitado':
            return {"erro": "Não é possível excluir uma conta que já foi quitada."}, 400

    try:
        BillRepository.delete(conta)
        return {"mensagem": "Conta excluída com sucesso!"}, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro ao excluir a conta."}, 500

    @staticmethod
    def pay_bill(user_id, company_id, bill_id):
        if not BillService._validate_user_company_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        conta = Bill.query.filter_by(bill_id=bill_id, company_id=company_id).first()

def pay_bill(user_id, bill_id):
    company_id = _get_company_id(user_id)
    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400
    conta = BillRepository.get_by_id_and_company(bill_id, company_id)

    if not conta:
        return {"erro": "Conta não encontrada"}, 404

    if conta.status == 'quitado':
        return {"erro": "Esta conta já está quitada."}, 400

    conta.status = 'quitado'
    conta.payment_date = date.today()

    try:
        BillRepository.save(conta)

        TransactionRepository.create(
            description=f"Quitação: {conta.description}",
            amount=conta.amount,
            date=conta.payment_date,
            type='despesa',
            company_id=company_id,
            user_id=user_id,
            category_id=conta.category_id,
            bill_id=conta.bill_id,
            type='despesa' if conta.type == 'pagar' else 'receita'
        )

        return {"mensagem": "Conta quitada e transação gerada com sucesso!"}, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro interno ao processar o pagamento."}, 500