from app.services.comparison_service import ComparisonService


def test_price_table_taxa_zero_parcela_igual_valor_sobre_prazo():
    pmt, total, interest = ComparisonService._calculate_price_table(1200, 0, 12)

    assert pmt == 100.0
    assert total == 1200.0
    assert interest == 0.0


def test_price_table_com_juros_gera_juros_positivo():
    pmt, total, interest = ComparisonService._calculate_price_table(12000, 2.0, 12)

    assert interest > 0
    assert total > 12000
