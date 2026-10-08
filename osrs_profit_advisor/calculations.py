from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any


def ge_tax(gross_revenue: float, max_tax: float = 5_000_000.0, rate: float = 0.02) -> float:
    """Return the Grand Exchange tax for a sale, capped at the OSRS limit."""
    return min(float(gross_revenue) * rate, max_tax)


def calculate_material_cost(material_prices: list[float] | tuple[float, ...], material_quantities: list[int] | tuple[int, ...]) -> float:
    if len(material_prices) != len(material_quantities):
        raise ValueError("material_prices and material_quantities must have the same length")
    return sum(price * qty for price, qty in zip(material_prices, material_quantities))


def calculate_profit(
    material_cost: float,
    sale_price: float,
    quantity: float,
    additional_costs: float = 0.0,
    tax_rate: float = 0.02,
    max_tax: float = 5_000_000.0,
) -> dict[str, float]:
    """Return a dictionary of profit metrics for a recipe or item sale."""
    gross_revenue = sale_price * quantity
    tax = min(gross_revenue * tax_rate, max_tax)
    net_profit = gross_revenue - tax - material_cost - additional_costs
    roi = (net_profit / material_cost * 100.0) if material_cost else 0.0
    return {
        "material_cost": float(material_cost),
        "gross_revenue": float(gross_revenue),
        "ge_tax": float(tax),
        "additional_costs": float(additional_costs),
        "net_profit": float(net_profit),
        "profit_per_unit": float(net_profit / quantity) if quantity else 0.0,
        "roi_percent": float(roi),
    }


def expected_output(quantity: float, success_probability: float) -> float:
    """Expected output for recipes with a chance of failure."""
    return quantity * success_probability


def is_missing_price(price: Any) -> bool:
    if price is None:
        return True
    if isinstance(price, (int, float)) and math.isnan(price):
        return True
    return False


def is_data_stale(last_updated: str | datetime | None, max_age_seconds: int = 1800) -> bool:
    """Return True if the price dataset is older than the allowed maximum age."""
    if last_updated is None:
        return True

    if isinstance(last_updated, datetime):
        timestamp = last_updated
    else:
        try:
            timestamp = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
        except ValueError:
            return True

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    age = datetime.now(timezone.utc) - timestamp
    return age.total_seconds() > max_age_seconds


def validate_api_response(payload: Any) -> bool:
    """Basic validation for malformed or incomplete API payloads."""
    if not isinstance(payload, dict):
        return False
    if not payload:
        return False
    if "data" not in payload and "items" not in payload:
        return False
    return True


def has_insufficient_history(points: list[float], minimum_points: int = 10) -> bool:
    return len(points) < minimum_points


def forecast_warning_for_volume(volume: float | None, minimum_volume: float = 1000.0) -> bool:
    if volume is None:
        return True
    return float(volume) < minimum_volume


def price_trend_direction(history: list[float]) -> str:
    if len(history) < 2:
        return "insufficient_data"
    first = history[0]
    last = history[-1]
    if last > first:
        return "upward"
    if last < first:
        return "downward"
    return "flat"
