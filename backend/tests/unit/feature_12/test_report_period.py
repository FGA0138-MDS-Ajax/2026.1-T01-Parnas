import pytest
from datetime import date

from app.services.report_service import ReportService


def test_period_dates_mensal_calcula_inicio_e_fim_do_mes():
    start, end = ReportService.get_period_dates({"period": "mensal", "month": 6, "year": 2026})

    assert start == date(2026, 6, 1)
    assert end == date(2026, 6, 30)


def test_period_dates_anual_cobre_ano_inteiro():
    start, end = ReportService.get_period_dates({"period": "anual", "year": 2026})

    assert (start, end) == (date(2026, 1, 1), date(2026, 12, 31))


def test_period_dates_personalizado_usa_datas_informadas():
    dados = {"start_date": date(2026, 3, 1), "end_date": date(2026, 3, 15)}

    assert ReportService.get_period_dates(dados) == (date(2026, 3, 1), date(2026, 3, 15))


def test_period_dates_mensal_sem_mes_ou_ano_levanta_erro():
    with pytest.raises(ValueError):
        ReportService.get_period_dates({"period": "mensal", "year": 2026})


def test_period_dates_start_posterior_a_end_levanta_erro():
    with pytest.raises(ValueError):
        ReportService.get_period_dates({"start_date": date(2026, 5, 10), "end_date": date(2026, 5, 1)})


def test_period_dates_sem_parametros_levanta_erro():
    with pytest.raises(ValueError):
        ReportService.get_period_dates({})
