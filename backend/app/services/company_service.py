import re
from datetime import date
from app.repositories.company_repository import CompanyRepository


def register_company(user_id, data):
    try:
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        phone = data.get('phone')

        cnpj_clean = re.sub(r'\D', '', cnpj) if cnpj else ""

        if CompanyRepository.get_by_cnpj(cnpj_clean):
            return {"erro": "CNPJ já cadastrado"}, 409

        new_company = CompanyRepository.create(
            name=name,
            cnpj=cnpj_clean,
            email=email,
            phone=phone,
            register_date=date.today()
        )

        CompanyRepository.attach_user(new_company.company_id, user_id)

        return {
            "mensagem": "Empresa cadastrada com sucesso",
            "company_id": new_company.company_id,
            "name": new_company.name,
            "cnpj": new_company.cnpj
        }, 201

    except Exception as e:
        print(f"Erro ao cadastrar empresa: {str(e)}")
        return {"erro": f"Ocorreu um erro interno ao tentar cadastrar a empresa: {str(e)}"}, 500


def delete_company(cnpj, user_id):
    cnpj_clean = re.sub(r'\D', '', cnpj) if cnpj else ""
    company = CompanyRepository.get_by_cnpj(cnpj_clean)

    if not company:
        return {"erro": "Empresa não encontrada."}, 404

    if not CompanyRepository.check_user_access(company.company_id, user_id):
        return {"erro": "Acesso negado. Você não tem permissão para excluir esta empresa."}, 403

    try:
        CompanyRepository.delete(company)
        return {"mensagem": "Empresa excluída com sucesso."}, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro interno ao tentar excluir a empresa."}, 500


def update_company(cnpj, data, user_id):
    cnpj_clean = re.sub(r'\D', '', cnpj) if cnpj else ""
    company = CompanyRepository.get_by_cnpj(cnpj_clean)

    if not company:
        return {"erro": "Empresa não encontrada."}, 404

    if not CompanyRepository.check_user_access(company.company_id, user_id):
        return {"erro": "Acesso negado. Você não tem permissão para alterar esta empresa."}, 403

    novo_cnpj = data.get('cnpj')
    if novo_cnpj:
        novo_cnpj_clean = re.sub(r'\D', '', novo_cnpj)
        if novo_cnpj_clean != company.cnpj:
            if CompanyRepository.get_by_cnpj(novo_cnpj_clean):
                return {"erro": "Este CNPJ já está em uso por outra empresa."}, 409
            company.cnpj = novo_cnpj_clean

    if 'name' in data:
        company.name = data['name']

    try:
        CompanyRepository.save(company)
        return {"mensagem": "Dados do empresa atualizados com sucesso."}, 200
    except Exception as e:
        return {"erro": "Ocorreu um erro interno ao tentar atualizar a empresa."}, 500