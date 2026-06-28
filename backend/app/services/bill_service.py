from datetime import date, datetime
from app.repositories.bill_repository import BillRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.company_repository import CompanyRepository

class BillService:

    @staticmethod
    def create_bill(user_id, company_id, data):
        if not company_id:
            return{"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

        if not CompanyRepository.check_user_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        try:
            nova_conta = BillRepository.create(
                company_id=company_id,
                description=data['description'],
                amount=data['amount'],
                type=data['type'],
                due_date=data['due_date'],
                category_id=data['category_id']
            )
            return {"mensagem": "Conta criada com sucesso!", "id": nova_conta.bill_id}, 201
        except Exception as e:
            return {"erro": "Ocorreu um erro interno ao criar a conta."}, 500

    @staticmethod
    def get_bills(user_id, company_id, status=None):
        if not company_id:
            return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

        if not CompanyRepository.check_user_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        contas = BillRepository.list_by_company(company_id, status=status)

        resultado = [{
            "id": c.bill_id,
            "description": c.description,
            "amount": float(c.amount),
            "type": c.type,
            "status": c.status,
            "due_date": c.due_date.isoformat() if c.due_date else None,
            "payment_date": c.payment_date.isoformat() if c.payment_date else None,
            "category_id": c.category_id # anna: adicionado o ID da Categoria para o frontend ler
        } for c in contas]

        return resultado, 200

    @staticmethod
    def update_bill(user_id, company_id, bill_id, data):
        if not company_id:
            return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

        if not CompanyRepository.check_user_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        conta = BillRepository.get_by_id_and_company(bill_id, company_id)

        if not conta:
            return {"erro": "Conta não encontrada"}, 404

        if conta.status == 'quitado':
            return {"erro": "Não é possível editar uma conta que já foi quitada."}, 400

        conta.description = data.get('description', conta.description)
        conta.amount = data.get('amount', conta.amount)

        if 'due_date' in data:
            conta.due_date = data['due_date']
        if 'category_id' in data:
            conta.category_id = data['category_id']

        try:
            BillRepository.save(conta)
            return {"mensagem": "Conta atualizada com sucesso!"}, 200
        except Exception as e:
            return {"erro": "Ocorreu um erro interno ao atualizar a conta."}, 500

    @staticmethod
    def delete_bill(user_id, company_id, bill_id):
        if not company_id:
            return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

        if not CompanyRepository.check_user_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

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

    @staticmethod
    def pay_bill(user_id, company_id, bill_id):
        if not company_id:
            return {"erro": "Nenhuma empresa ativa selecionada na sessão."}, 400

        if not CompanyRepository.check_user_access(user_id, company_id):
            return {"erro": "Acesso negado a esta empresa."}, 403

        conta = BillRepository.get_by_id_and_company(bill_id, company_id)

        if not conta:
            return {"erro": "Conta não encontrada"}, 404

        if conta.status == 'quitado':
            return {"erro": "Esta conta já está quitada."}, 400

        conta.status = 'quitado'
        conta.payment_date = date.today()

        try:
            BillRepository.save(conta)

            #anna: enviando os 7 dados de forma ESTRITAMENTE POSICIONAL (só assim o front consome corretamebre)
            try:
                TransactionRepository.create(
                    f"Quitação: {conta.description}",
                    conta.amount,
                    conta.payment_date,
                    'despesa' if conta.type == 'pagar' else 'receita',
                    company_id,
                    user_id,
                    conta.category_id,
                    conta.bill_id 
                )
            except TypeError:
                TransactionRepository.create(
                    f"Quitação: {conta.description}",
                    conta.amount,
                    conta.payment_date,
                    'despesa' if conta.type == 'pagar' else 'receita',
                    company_id,
                    user_id,
                    conta.category_id
                )

            return {"mensagem": "Conta quitada e transação gerada com sucesso!"}, 200
        except Exception as e:
            print(f"Erro ao gerar transação de quitação: {e}")
            return {"erro": "Ocorreu um erro interno ao processar o pagamento."}, 500