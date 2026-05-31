from app.models.transaction import Transaction
from app.config import db
from sqlalchemy import func

class TransactionService:
    @staticmethod
    def get_history(user_id, page, per_page, filtros):
        # 1. Filtro obrigatório: apenas transações do usuário logado
        condicoes = [Transaction.user_id == user_id]

        # 2. Filtros dinâmicos da URL
        if filtros.get('data_inicio'):
            condicoes.append(Transaction.date >= filtros['data_inicio'])
        if filtros.get('data_fim'):
            condicoes.append(Transaction.date <= filtros['data_fim'])
        if filtros.get('tipo'):
            condicoes.append(Transaction.type == filtros['tipo'])
        if filtros.get('categoria'):
            condicoes.append(Transaction.category.ilike(f"%{filtros['categoria']}%"))
        if filtros.get('valor_min') is not None:
            condicoes.append(Transaction.amount >= filtros['valor_min'])
        if filtros.get('valor_max') is not None:
            condicoes.append(Transaction.amount <= filtros['valor_max'])

        # Query base para listar os itens
        query_base = Transaction.query.filter(*condicoes)

        # 3. Cálculo de Totais (Agregação no Banco)
        totais = db.session.query(
            Transaction.type, func.sum(Transaction.amount)
        ).filter(*condicoes).group_by(Transaction.type).all()

        receitas = sum(valor for tipo, valor in totais if tipo == 'receita') or 0.0
        despesas = sum(valor for tipo, valor in totais if tipo == 'despesa') or 0.0
        saldo = receitas - despesas

        # 4. Paginação dos resultados
        paginacao = query_base.order_by(Transaction.date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        # 5. Formatação da lista
        transacoes_lista = [{
            "id": t.id,
            "tipo": t.type,
            "categoria": t.category,
            "valor": float(t.amount),
            "data": t.date.isoformat() if t.date else None
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
