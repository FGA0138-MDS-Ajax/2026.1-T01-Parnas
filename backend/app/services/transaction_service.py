from app.repositories.transaction_repository import TransactionRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.company_repository import CompanyRepository
from app.exceptions.api_exception import APIException

class TransactionService:
    @staticmethod
    def get_history_filtered(user_id, company_id, page, per_page, filtros):

        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

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
            "type": t.type,
            "category_id": t.category_id,
            "amount": float(t.amount),
            "date": t.date.strftime("%Y-%m-%d") if t.date else None,
            "bill_id": t.bill_id,
            "payment_id": t.payment_id  # anna correção: enviando o ID do banco para o front
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

    @staticmethod
    def create_transaction(user_id, company_id, data):
        category_id = data.get('category_id')

        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

        category = CategoryRepository.get_by_id_and_company(category_id, company_id)
        if not category:
            raise APIException("A categoria informada não existe ou não pertence a esta empresa.", 400)

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

            if 'payment_id' in data and data['payment_id']:
                from app.config import db
                from app.models.transaction import Transaction
                
                db.session.query(Transaction).filter(
                    Transaction.transaction_id == new_transaction.transaction_id
                ).update({"payment_id": int(data['payment_id'])})
                
                db.session.commit()

            return {
                "mensagem": "Transação registrada com sucesso.",
                "transaction_id": new_transaction.transaction_id
            }, 201
        except ValueError as ve:
            return {"erro": str(ve)}, 400
        except Exception as e:
            print(f"Erro interno ao salvar transação: {e}")
            return {"erro": "Ocorreu um erro interno ao registrar transação."}, 500


    @staticmethod
    def get_company_transactions(user_id, company_id):

        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)

        transactions = TransactionRepository.list_by_company_and_user(company_id, user_id)
        return {"transactions_objects": transactions}, 200


    @staticmethod
    def update_transaction(user_id, company_id, transaction_id, data):
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)
        
        access = CompanyRepository.check_user_access(company_id, user_id)
        if not access:
            raise APIException("Acesso negado. Você não tem permissão para acessar esta empresa.", 403)
        
        transaction = TransactionRepository.get_by_id_and_user(transaction_id, user_id)
        if not transaction:
            raise APIException("Transação não encontrada", 404)

        if 'category_id' in data:
            category = CategoryRepository.get_by_id_and_company(data['category_id'], company_id)
            if not category:
                raise APIException("A categoria informada não pertence à empresa desta transação.", 400)
            transaction.category_id = data['category_id']
        if 'description' in data:
            transaction.description = data['description']
        if 'amount' in data:
            transaction.amount = data['amount']
        if 'date' in data:
            transaction.date = data['date']
        if 'type' in data:
            transaction.type = data['type']

        # anna: atualiza a conta/caixa na edição também se enviado
        if 'payment_id' in data:
            transaction.payment_id = data['payment_id']

        try:
            TransactionRepository.save(transaction)
            return {
                "mensagem": "Transação actualizada com sucesso.",
                "transaction": transaction
            }, 200
        except Exception as e:
            return {"erro": f"Ocorreu um erro interno ao tentar atualizar a transação: {str(e)}"}, 500


    @staticmethod
    def delete_transaction(user_id, transaction_id):
        transaction = TransactionRepository.get_by_id_and_user(transaction_id, user_id)
        if not transaction:
            return {"erro": "Transação não encontrada ou você não possui permissão para excluí-la."}, 404

        try:
            TransactionRepository.delete_instance(transaction)
            return {"mensagem": "Transação excluída com sucesso."}, 200
        except Exception as e:
            return {"erro": f"Ocorreu um erro interno ao tentar excluir a transação: {str(e)}"}, 500