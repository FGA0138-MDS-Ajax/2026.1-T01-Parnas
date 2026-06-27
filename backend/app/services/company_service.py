import re

from app.config import db
from app.exceptions.api_exception import APIException
from app.repositories.company_repository import CompanyRepository


def _api_error(error):
    return {"erro": error.message}, error.status_code


def register_company(user_id, data):
    try:
        cnpj = data.get("cnpj")

        if CompanyRepository.get_by_cnpj(cnpj):
            raise APIException("CNPJ já cadastrado.", 409)

        company = CompanyRepository.create(
            name=data.get("name"),
            cnpj=cnpj,
            email=data.get("email"),
            phone=data.get("phone"),
            user_id=user_id,
        )

        return {
            "mensagem": "Empresa cadastrada com sucesso",
            "company_id": company.company_id,
            "name": company.name,
            "cnpj": company.cnpj,
        }, 201
    except APIException as error:
        return _api_error(error)
    except Exception as error:
        db.session.rollback()
        print(f"Erro ao cadastrar empresa: {error}")
        return {
            "erro": (
                "Ocorreu um erro interno ao tentar cadastrar a empresa: "
                f"{error}"
            )
        }, 500


def delete_company(company_id, user_id):
    try:
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        CompanyRepository.check_access(company_id, user_id)
        CompanyRepository.delete(company_id)

        return {"mensagem": "Empresa deletada com sucesso."}, 200
    except APIException as error:
        return _api_error(error)
    except Exception as error:
        db.session.rollback()
        print(f"Erro ao deletar empresa: {error}")
        return {
            "erro": (
                "Ocorreu um erro interno ao tentar deletar a empresa: "
                f"{error}"
            )
        }, 500


def update_company(data, user_id, company_id):
    try:
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        CompanyRepository.check_access(company_id, user_id)

        if "cnpj" in data:
            cnpj = re.sub(r"\D", "", data["cnpj"])
            existing_company = CompanyRepository.get_by_cnpj(cnpj)
            if (
                existing_company
                and existing_company.company_id != company_id
            ):
                raise APIException("CNPJ já cadastrado.", 409)
            company.cnpj = cnpj

        for field in ("name", "email", "phone"):
            if field in data:
                setattr(company, field, data[field])

        db.session.commit()
        return {
            "mensagem": "Dados da empresa atualizados com sucesso.",
            "company": company,
        }, 200
    except APIException as error:
        return _api_error(error)
    except Exception as error:
        db.session.rollback()
        print(f"Erro ao atualizar empresa: {error}")
        return {
            "erro": (
                "Ocorreu um erro interno ao tentar atualizar a empresa: "
                f"{error}"
            )
        }, 500


def get_company(company_id, user_id):
    try:
        company = CompanyRepository.get_by_id(company_id)
        if not company:
            raise APIException("Empresa não encontrada.", 404)

        CompanyRepository.check_access(company_id, user_id)
        return {"company": company}, 200
    except APIException as error:
        return _api_error(error)
    except Exception as error:
        print(f"Erro ao buscar empresa: {error}")
        return {
            "erro": (
                "Ocorreu um erro interno ao tentar buscar a empresa: "
                f"{error}"
            )
        }, 500


def get_all_companies(user_id):
    try:
        companies = CompanyRepository.get_all_by_user(user_id)
        return {"companies": companies}, 200
    except APIException as error:
        return _api_error(error)
    except Exception as error:
        print(f"Erro ao buscar empresas: {error}")
        return {
            "erro": (
                "Ocorreu um erro interno ao tentar buscar as empresas: "
                f"{error}"
            )
        }, 500
