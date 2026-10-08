from __future__ import annotations

from osrs_profit_advisor.calculations import ge_tax, calculate_profit, expected_output, is_missing_price, is_data_stale, validate_api_response, has_insufficient_history, forecast_warning_for_volume


def test_ge_tax_basic() -> None:
    assert ge_tax(1000) == 20.0


def test_ge_tax_cap() -> None:
    assert ge_tax(1_000_000_000) == 5_000_000.0


def test_calculate_profit() -> None:
    result = calculate_profit(material_cost=1000, sale_price=1200, quantity=2, additional_costs=50)
    assert result["material_cost"] == 1000.0
    assert result["gross_revenue"] == 2400.0
    assert result["ge_tax"] == 48.0
    assert result["net_profit"] == 1302.0
    assert result["roi_percent"] == 130.2


def test_roi_with_zero_material_cost() -> None:
    result = calculate_profit(material_cost=0, sale_price=1500, quantity=1)
    assert result["roi_percent"] == 0.0


def test_negative_profit_recipe() -> None:
    result = calculate_profit(material_cost=5000, sale_price=4000, quantity=1)
    assert result["net_profit"] < 0


def test_expected_output_with_failure() -> None:
    expected = expected_output(10, 0.75)
    assert expected == 7.5


def test_missing_price() -> None:
    assert is_missing_price(None) is True
    assert is_missing_price(1200) is False


def test_stale_data() -> None:
    from datetime import datetime, timedelta, timezone

    stale_time = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    assert is_data_stale(stale_time, max_age_seconds=1800) is True


def test_invalid_api_response() -> None:
    assert validate_api_response({}) is False
    assert validate_api_response({"data": [{"id": 1}]}) is True


def test_insufficient_history() -> None:
    assert has_insufficient_history([1, 2, 3], minimum_points=5) is True
    assert has_insufficient_history([1, 2, 3, 4, 5], minimum_points=5) is False


def test_low_volume_warning() -> None:
    assert forecast_warning_for_volume(500) is True
    assert forecast_warning_for_volume(5000) is False
