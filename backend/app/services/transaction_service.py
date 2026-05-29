from app.config import db
from app.models import category
from app.models. transaction import Transaction
from app.models.category import Category

def create_transaction(data, current_user_id):
    category = Category.query.filter_by(
        category_id=data['category_id'],
        company_id=data['company_id']
    ).first()

    if not category:
        return {"erro": "A categoria informada não existe ou não pertence a esta empresa."}

    new_transaction = Transaction(
        description=data['description'],
        amount=data['amount'],
        date=data['date'],
        type=data['type'],
        company_id=data['company_id'],
        category_id=data['category_id'],
        user_id=current_user_id
    )

    try:
        db.session.add(new_transaction)
        db.session.commit()
        return {
            "mensagem": "Transação registrada com sucesso.",
            "transaction_id": new_transaction.transaction_id
        },201
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao registrar transação."}, 500

def get_company_transactions(company_id):
    transactions = Transaction.query.filter_by(company_id=company_id).all()

    result = []
    for t in transactions:
        result.append({
            "transaction_id": t.transaction_id,
            "description": t.description,
            "amount": float(t.amount),
            "date": t.date.strftime("%Y-%m-%d"),
            "type": t.type,
            "category_id": t.category_id,
        })

    return {"transactions": result}, 200

def update_transaction(transaction_id, data, company_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id, company_id=company_id).first()

    if not transaction:
        return {"erro": "Transação não encontrada nesta empresa."}, 404

    if 'description' in data:
        transaction.description = data['description']
    if 'amount' in data:
        transaction.amount = data['amount']
    if 'date' in data:
        transaction.date = data['date']
    if 'type' in data:
        transaction.type = data['type']
    if 'category_id' in data:
        transaction.category_id = data['category_id']

    try:
        db.session.commit()
        return {"mensagem": "Transação atualizada com sucesso."}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro ao atualizar"}, 500

def delete_transaction(transaction_id, company_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id, company_id=company_id).first()

    if not transaction:
        return {"erro": "Transação não encontrada nesta empresa."}, 404

    try:
        db.session.delete(transaction)
        db.session.commit()
        return {"mensagem": "Transação excluída com sucesso."}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro ao excluir a transação."}, 500