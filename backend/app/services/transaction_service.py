from app.repositories.transaction_repository import TransactionRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository


def _get_company_id(user_id):
    user = UserRepository.get_by_id(user_id)
    return user.active_company_id if user else None


def get_history_filtered(user_id, page, per_page, filtros):
    company_id = _get_company_id(user_id)
    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    filtros['user_id'] = user_id

    query_base, totais = TransactionRepository.get_filtered_history_query(
        filtros,
        categoria_nome=filtros.get('categoria')
    )

    receitas = sum(float(valor) for tipo, valor in totais if tipo == 'receita')
    despesas = sum(float(valor) for tipo, valor in totais if tipo == 'despesa')
    saldo = receitas - despesas

    paginacao = query_base.order_by(TransactionRepository.model.date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    transacoes_lista = [{
        "transaction_id": t.transaction_id,
        "description": t.description,
        "tipo": t.type,
        "categoria_id": t.category_id,
        "valor": float(t.amount),
        "data": t.date.strftime("%Y-%m-%d") if t.date else None,
        "id_conta": t.bill_id
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
    company_id = _get_company_id(user_id)
    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    category = CategoryRepository.get_by_id_and_company(category_id, company_id)
    if not category:
        return {"erro": "A categoria informada não existe ou não pertence a esta empresa."}, 400

    try:
        new_transaction = TransactionRepository.create(
            description=data['description'],
            amount=data['amount'],
            date=data['date'],
            type=data['type'],
            company_id=company_id,
            category_id=category_id,
            user_id=user_id
        )
        return {
            "mensagem": "Transação registrada com sucesso.",
            "transaction_id": new_transaction.transaction_id
        }, 201
    except ValueError as ve:
        return {"erro": str(ve)}, 400
    except Exception as e:
        return {"erro": "Ocorreu um erro interno ao registrar transação."}, 500


def get_company_transactions(user_id):
    company_id = _get_company_id(user_id)
    if not company_id:
        return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

    transactions = TransactionRepository.list_by_company_and_user(company_id, user_id)
    return {"transactions_objects": transactions}, 200


def update_transaction(transaction_id, user_id, data):
    transaction = TransactionRepository.get_by_id_and_user(transaction_id, user_id)
    if not transaction:
        return {"erro": "Transação não encontrada ou você não possui permissão para alterá-la."}, 404

    if 'category_id' in data:
        category = CategoryRepository.get_by_id_and_company(data['category_id'], transaction.company_id)
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
        TransactionRepository.save(transaction)
        return {
            "mensagem": "Transação actualizada com sucesso.",
            "transaction": transaction
        }, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro interno ao atualizar a transação."}, 500


def delete_transaction(transaction_id, user_id):
    transaction = TransactionRepository.get_by_id_and_user(transaction_id, user_id)
    if not transaction:
        return {"erro": "Transação não encontrada ou você não possui permissão para excluí-la."}, 404

    try:
        TransactionRepository.delete_instance(transaction)
        return {"mensagem": "Transação excluída com sucesso."}, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro ao excluir a transação."}, 500