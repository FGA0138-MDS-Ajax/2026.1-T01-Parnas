from app.services.comparison_service import ComparisonService


def _mod(name="Banco A", rate=2.0, term=12, tipo="PJ"):
    return {"name": name, "interest_rate": rate, "term_months": term, "type": tipo}


def test_price_table_taxa_zero_parcela_igual_valor_sobre_prazo():
    pmt, total, interest = ComparisonService._calculate_price_table(1200, 0, 12)

    assert pmt == 100.0
    assert total == 1200.0
    assert interest == 0.0


def test_price_table_com_juros_gera_juros_positivo():
    pmt, total, interest = ComparisonService._calculate_price_table(12000, 2.0, 12)

    assert interest > 0
    assert total > 12000


def test_calculate_simulation_marca_a_de_menor_custo_como_melhor():
    data = {"loan_amount": 10000, "modalities": [_mod("Cara", rate=5.0), _mod("Barata", rate=1.0)]}

    res, status = ComparisonService.calculate_simulation(data)

    assert status == 200
    melhores = [c for c in res["comparisons"] if c["is_best_option"]]
    assert len(melhores) == 1
    assert melhores[0]["name"] == "Barata"


def test_calculate_simulation_sinaliza_modalidade_pf():
    data = {"loan_amount": 10000, "modalities": [_mod(tipo="pf")]}

    res, _ = ComparisonService.calculate_simulation(data)

    assert res["comparisons"][0]["warning_pf"] is True
    assert res["comparisons"][0]["type"] == "PF"


def test_calculate_simulation_pj_nao_dispara_alerta():
    data = {"loan_amount": 10000, "modalities": [_mod(tipo="PJ")]}

    res, _ = ComparisonService.calculate_simulation(data)

    assert res["comparisons"][0]["warning_pf"] is False


def test_calculate_simulation_sem_modalidades_retorna_400():
    res, status = ComparisonService.calculate_simulation({"loan_amount": 10000, "modalities": []})

    assert status == 400


def test_calculate_simulation_acima_de_4_modalidades_retorna_400():
    data = {"loan_amount": 10000, "modalities": [_mod(name=f"M{i}") for i in range(5)]}

    res, status = ComparisonService.calculate_simulation(data)

    assert status == 400
