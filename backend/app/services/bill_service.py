from datetime import date, datetime
from app.repositories.bill_repository import BillRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository


def _get_company_id(user_id):
    user = UserRepository.get_by_id(user_id)
    return user.active_company_id if user else None


def create_bill(user_id, data):
    company_id = _get_company_id(user_id)

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


def get_bills(user_id, status=None):
    company_id = _get_company_id(user_id)
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

    return resultado, 200


def update_bill(user_id, bill_id, data):
    company_id = _get_company_id(user_id)
    conta = BillRepository.get_by_id_and_company(bill_id, company_id)

    if not conta:
        return {"erro": "Conta não encontrada"}, 404

    if conta.status == 'quitado':
        return {"erro": "Não é possível editar uma conta que já foi quitada."}, 400

    conta.description = data.get('description', conta.description)
    conta.amount = data.get('amount', conta.amount)
    if 'due_date' in data:
        conta.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()

    try:
        BillRepository.save(conta)
        return {"mensagem": "Conta atualizada com sucesso!"}, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro interno ao atualizar a conta."}, 500


def delete_bill(user_id, bill_id):
    company_id = _get_company_id(user_id)
    conta = BillRepository.get_by_id_and_company(bill_id, company_id)

    if not conta:
        return {"erro": "Conta não encontrada"}, 404

    if conta.status == 'quitado':
        return {"erro": "Não é possível excluir uma conta que já foi quitada."}, 400

    try:
        BillRepository.delete(conta)
        return {"mensagem": "Conta excluída com sucesso!"}, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro ao excluir a conta."}, 500


def pay_bill(user_id, bill_id):
    company_id = _get_company_id(user_id)
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
            category_id=conta.category_id
        )

        return {"mensagem": "Conta quitada e transação gerada com sucesso!"}, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro interno ao processar o pagamento."}, 500