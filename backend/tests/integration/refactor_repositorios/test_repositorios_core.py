"""Testes de QA do PR #79 - núcleo da camada de repositórios (refactor banco/rotas).

Por ser um PR gigante (e que aponta para a main), este arquivo foca no núcleo da
refatoração: a camada de repositórios (BaseRepository, UserRepository,
CompanyRepository), exercitada contra o BD em memória. Não cobre todas as 46 frentes
do PR - ver ressalvas no relatório de QA.
"""
import pytest
from datetime import date

from app.repositories.base_repository import BaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.company_repository import CompanyRepository
from app.models.company import Company


class TestBaseRepository:

    def test_save_find_e_delete(self, clean_db, app_context):
        repo = BaseRepository(Company)
        empresa = Company(
            name="Repo Co", cnpj="99888777000166",
            email="repo@co.com", phone="1130000000", register_date=date.today(),
        )
        salva = repo.save(empresa)
        assert salva.company_id is not None

        encontrada = repo.find_by_id(salva.company_id)
        assert encontrada.company_id == salva.company_id

        repo.delete(salva)
        assert repo.find_by_id(salva.company_id) is None


class TestUserRepository:

    def test_get_by_email_e_cpf(self, clean_db, test_user, app_context):
        assert UserRepository.get_by_email(test_user.email).user_id == test_user.user_id
        assert UserRepository.get_by_cpf(test_user.cpf).user_id == test_user.user_id

    def test_update_active_company(self, clean_db, test_company, test_user, app_context):
        ok = UserRepository.update_active_company(test_user.user_id, test_company.company_id)
        assert ok is True
        assert UserRepository.get_by_id(test_user.user_id).active_company_id == test_company.company_id

    def test_list_companies(self, clean_db, test_company, test_user, app_context):
        empresas = UserRepository.list_companies(test_user.user_id)
        assert any(c.company_id == test_company.company_id for c in empresas)


class TestCompanyRepository:

    def test_create_e_get_by_id(self, clean_db, app_context):
        empresa = CompanyRepository.create(
            "Mercado X", "11222333000181", "x@merc.com", "1140000000", date.today()
        )
        assert empresa.company_id is not None
        assert CompanyRepository.get_by_id(empresa.company_id).name == "Mercado X"

    def test_get_by_cnpj_limpa_formatacao(self, clean_db, app_context):
        CompanyRepository.create(
            "Mercado Y", "11222333000181", "y@merc.com", "1140000000", date.today()
        )
        # busca com CNPJ formatado deve encontrar (o repositório limpa antes de comparar)
        assert CompanyRepository.get_by_cnpj("11.222.333/0001-81") is not None

    def test_attach_user_e_check_access(self, clean_db, test_user, app_context):
        empresa = CompanyRepository.create(
            "Mercado Z", "45997418000153", "z@merc.com", "1140000000", date.today()
        )
        assert CompanyRepository.check_user_access(empresa.company_id, test_user.user_id) is False

        CompanyRepository.attach_user(empresa.company_id, test_user.user_id)
        assert CompanyRepository.check_user_access(empresa.company_id, test_user.user_id) is True

        empresas = CompanyRepository.get_all_by_user(test_user.user_id)
        assert any(c.company_id == empresa.company_id for c in empresas)
