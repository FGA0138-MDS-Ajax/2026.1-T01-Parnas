from app.repositories.transaction_repository import TransactionRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository  # Se houver um UserRepository para carregar o usuário

def _validate_user_company_access(user_id, company_id):
    """Verifica se o usuário tem acesso à empresa informada."""
    user = UserRepository.get_by_id(user_id)
    user_companies_ids = [c.company_id for c in user.companies] if user else []
    return company_id in user_companies_ids

def get_history_filtered(user_id, page, per_page, filtros):
    company_id = filtros.get('company_id')
    if not _validate_user_company_access(user_id, company_id):
        return {"erro": "Você não tem permissão para acessar os dados desta empresa."}, 403

    condicoes = [
        TransactionRepository.model.user_id == user_id,  # Referenciando via mapeamento do ORM
        TransactionRepository.model.company_id == company_id
    ]

    if filtros.get('data_inicio'):
        condicoes.append(TransactionRepository.model.date >= filtros['data_inicio'])
    if filtros.get('data_fim'):
        condicoes.append(TransactionRepository.model.date <= filtros['data_fim'])
    if filtros.get('tipo'):
        condicoes.append(TransactionRepository.model.type == filtros['tipo'])
    if filtros.get('valor_min') is not None:
        condicoes.append(TransactionRepository.model.amount >= filtros['valor_min'])
    if filtros.get('valor_max') is not None:
        condicoes.append(TransactionRepository.model.amount <= filtros['valor_max'])

    query_base, totais = TransactionRepository.get_filtered_history_query(
        condicoes,
        categoria_nome=filtros.get('categoria')
    )

    receitas = sum(valor for tipo, valor in totais if tipo == 'receita') or 0.0
    despesas = sum(valor for tipo, valor in totais if tipo == 'despesa') or 0.0
    saldo = receitas - despesas

    paginacao = query_base.order_by(TransactionRepository.model.date.desc()).paginate(page=page, per_page=per_page, error_out=False)

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
    company_id = data.get('company_id')

    if not _validate_user_company_access(user_id, company_id):
        return {"erro": "Você não tem permissão para lançar transações nesta empresa."}, 403

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


def get_company_transactions(company_id, user_id):
    if not _validate_user_company_access(user_id, company_id):
        return {"erro": "Você não tem permissão para visualizar transações nesta empresa."}, 403

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