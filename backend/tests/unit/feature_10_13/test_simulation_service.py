from unittest.mock import patch, MagicMock
from datetime import date

from app.services.simulation_service import (
    calculate_table_price,
    calculate_table_sac,
    process_simulation,
    project_impact_cash_flow,
)


def _dados(modality="PRICE", main=12000.0, rate=2.0, term=12):
    return {
        "requested_amount": main,
        "interest_rate": rate,
        "deadline_month": term,
        "modality": modality,
    }


def test_price_taxa_zero_parcela_igual_valor_sobre_prazo():
    parcelas, pmt = calculate_table_price(1200.0, 0, 12)

    assert round(pmt, 2) == 100.0
    assert all(p["juros"] == 0 for p in parcelas)


def test_price_parcelas_iguais_e_saldo_final_zera():
    parcelas, _ = calculate_table_price(12000.0, 2.0, 12)
    valores = [p["valor_parcela"] for p in parcelas]

    assert max(valores) == min(valores)
    assert abs(parcelas[-1]["saldo_devedor"]) <= 0.01


def test_sac_amortizacao_constante_e_saldo_final_zera():
    parcelas, _ = calculate_table_sac(12000.0, 2.0, 12)
    amortizacoes = [p["amortizacao"] for p in parcelas]

    assert max(amortizacoes) == min(amortizacoes)
    assert abs(parcelas[-1]["saldo_devedor"]) <= 0.01


def test_sac_parcelas_decrescentes():
    parcelas, _ = calculate_table_sac(12000.0, 2.0, 12)
    valores = [p["valor_parcela"] for p in parcelas]

    assert valores == sorted(valores, reverse=True)
    assert valores[0] > valores[-1]


def test_sac_paga_menos_juros_que_price_para_mesmos_parametros():
    price, _ = calculate_table_price(12000.0, 2.0, 12)
    sac, _ = calculate_table_sac(12000.0, 2.0, 12)

    assert sum(p["juros"] for p in sac) < sum(p["juros"] for p in price)


def test_process_simulation_price_resumo_coerente():
    res = process_simulation(_dados("PRICE"))
    resumo = res["resumo"]

    assert resumo["modalidade"] == "PRICE"
    assert len(res["detalhamento_mensal"]) == 12
    assert round(resumo["total_juros"], 2) == round(
        resumo["total_a_pagar"] - resumo["valor_solicitado"], 2
    )


def test_process_simulation_sem_company_id_nao_anexa_projecao():
    res = process_simulation(_dados("PRICE"))

    assert "projecao_fluxo_caixa" not in res


@patch("app.services.simulation_service.Transaction")
def test_process_simulation_com_company_id_anexa_projecao(mock_tx):
    mock_tx.query.filter_by.return_value.all.return_value = []

    res = process_simulation(_dados("PRICE"), company_id=1)

    assert res["projecao_fluxo_caixa"]["status"] == "Indisponível"


@patch("app.services.simulation_service.Transaction")
def test_projecao_sem_transacoes_indisponivel(mock_tx):
    mock_tx.query.filter_by.return_value.all.return_value = []

    proj = project_impact_cash_flow(1, 100.0)

    assert proj["status"] == "Indisponível"
    assert proj["comprometimento_perc"] is None


@patch("app.services.simulation_service.Transaction")
def test_projecao_empresa_lucrativa_saudavel(mock_tx):
    receita = MagicMock(amount=10000.0, type="receita", date=date(2025, 1, 10))
    despesa = MagicMock(amount=2000.0, type="despesa", date=date(2025, 1, 20))
    mock_tx.query.filter_by.return_value.all.return_value = [receita, despesa]

    proj = project_impact_cash_flow(1, 100.0)

    assert proj["status"] == "Saudável"
    assert proj["comprometimento_perc"] is not None


@patch("app.services.simulation_service.Transaction")
def test_projecao_empresa_no_prejuizo_alerta_vermelho(mock_tx):
    receita = MagicMock(amount=1000.0, type="receita", date=date(2025, 1, 10))
    despesa = MagicMock(amount=5000.0, type="despesa", date=date(2025, 1, 20))
    mock_tx.query.filter_by.return_value.all.return_value = [receita, despesa]

    proj = project_impact_cash_flow(1, 100.0)

    assert proj["status"] == "Alerta vermelho"
    assert proj["comprometimento_perc"] == 100.0
