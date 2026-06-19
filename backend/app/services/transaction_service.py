from app.config import db
from app.models.transaction import Transaction
from app.models.category import Category
from sqlalchemy import func
from flask_jwt_extended import get_jwt

def _get_active_company():
    claims = get_jwt()
    return claims.get("active_company_id")

def get_history_filtered(user_id, page, per_page, filtros):
    company_id = _get_active_company()
    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    condicoes = [
        Transaction.user_id == user_id,
        Transaction.company_id == company_id
    ]

    if filtros.get('data_inicio'):
        condicoes.append(Transaction.date >= filtros['data_inicio'])
    if filtros.get('data_fim'):
        condicoes.append(Transaction.date <= filtros['data_fim'])
    if filtros.get('tipo'):
        condicoes.append(Transaction.type == filtros['tipo'])
    if filtros.get('valor_min') is not None:
        condicoes.append(Transaction.amount >= filtros['valor_min'])
    if filtros.get('valor_max') is not None:
        condicoes.append(Transaction.amount <= filtros['valor_max'])

    query_base = Transaction.query.filter(*condicoes)

    if filtros.get('categoria'):
        query_base = query_base.join(Category).filter(Category.name.ilike(f"%{filtros['categoria']}%"))

    totais = db.session.query(
        Transaction.type, func.sum(Transaction.amount)
    ).filter(*condicoes).group_by(Transaction.type).all()

    receitas = sum(valor for tipo, valor in totais if tipo == 'receita') or 0.0
    despesas = sum(valor for tipo, valor in totais if tipo == 'despesa') or 0.0
    saldo = receitas - despesas

    paginacao = query_base.order_by(Transaction.date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    transacoes_lista = [{
        "transaction_id": t.transaction_id,
        "description": t.description,
        "tipo": t.type,
        "categoria_id": t.category_id,
        "valor": float(t.amount),
        "data": t.date.strftime("%Y-%m-%d") if t.date else None
    } for t in paginacao.items]

    return {
        "resumo": {
            "total_receitas": receitas,
            "total_despesas": despesas,
            "saldo": saldo
        },
        "paginacao": {
            "total_items": paginacao.total,
            "paginas": paginacao.pages,
            "pagina_atual": paginacao.page
        },
        "transacoes": transacoes_lista
    }, 200


def create_transaction(data, user_id):
    category_id = data.get('category_id')
    company_id = _get_active_company()
    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    category = Category.query.filter_by(
        category_id=data['category_id'],
        company_id=data['company_id']
    ).first()

    if not category:
        return {"erro": "A categoria informada não existe ou não pertence a esta empresa."}, 400

    new_transaction = Transaction(
        description=data['description'],
        amount=data['amount'],
        date=data['date'],
        type=data['type'],
        company_id=company_id,
        category_id=category_id,
        user_id=user_id
    )

    try:
        db.session.add(new_transaction)
        db.session.commit()
        return {
            "mensagem": "Transação registrada com sucesso.",
            "transaction_id": new_transaction.transaction_id
        }, 201
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao registrar transação."}, 500


def get_company_transactions(user_id):
    company_id = _get_active_company()
    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    transactions = Transaction.query.filter_by(company_id=company_id, user_id=user_id).all()
    return {"transactions_objects": transactions}, 200


def update_transaction(transaction_id, user_id, data):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id, user_id=user_id).first()
    if not transaction:
        return {"erro": "Transação não encontrada ou você não possui permissão para alterá-la."}, 404

    if 'category_id' in data:
        category = Category.query.filter_by(
            category_id=data['category_id'],
            company_id=transaction.company_id
        ).first()
        if not category:
            return {"erro": "A categoria informada não pertence à empresa desta transação."}, 400
        transaction.category_id = data['category_id']

    if 'description' in data:
        transaction.description = data['description']
    if 'amount' in data:
        transaction.amount = data['amount']
    if 'date' in data:
        transaction.date = data['date']
    if 'type' in data:
        transaction.type = data['type']

    try:
        db.session.commit()
        return {
            "mensagem": "Transação atualizada com sucesso.",
            "transaction": transaction
        }, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro interno ao atualizar a transação."}, 500


def delete_transaction(transaction_id, user_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id, user_id=user_id).first()

    if not transaction:
        return {"erro": "Transação não encontrada ou você não possui permissão para excluí-la."}, 404

    try:
        db.session.delete(transaction)
        db.session.commit()
        return {"mensagem": "Transação excluída com sucesso."}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": "Ocorreu um erro ao excluir a transação."}, 500