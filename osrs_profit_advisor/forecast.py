from __future__ import annotations

from typing import Iterable, Sequence


def moving_average(values: Sequence[float], window: int = 7) -> list[float]:
    if not values:
        return []
    window = max(1, min(window, len(values)))
    averages: list[float] = []
    for index in range(len(values)):
        start = max(0, index - window + 1)
        slice_values = list(values[start : index + 1])
        averages.append(sum(slice_values) / len(slice_values))
    return averages


def linear_trend_forecast(history: Sequence[float], periods: int = 24) -> list[float]:
    if len(history) < 2:
        return [float(history[-1]) for _ in range(periods)] if history else []

    delta = (history[-1] - history[0]) / max(1, len(history) - 1)
    forecast = []
    current = history[-1]
    for _ in range(periods):
        current += delta
        forecast.append(current)
    return forecast


def forecast_interval(history: Sequence[float], periods: int = 24) -> tuple[float, float]:
    if not history:
        return (0.0, 0.0)
    avg = sum(history) / len(history)
    volatility = max(1.0, (max(history) - min(history)) * 0.1)
    low = avg - volatility
    high = avg + volatility
    return (low, high)


def forecast_reliability(history: Sequence[float], volume: float | None = None) -> str:
    if len(history) < 10:
        return "premalo podatkov"
    if volume is not None and volume < 1000:
        return "nizka"
    return "visoka"


def volume_warning(volume: float | None) -> bool:
    return volume is None or float(volume) < 1000.0
