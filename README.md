# OSRS Profit Advisor

A Linux desktop application for tracking Old School RuneScape Grand Exchange prices, recipe profitability, and price forecasting.

This repository is being built incrementally. The first step establishes the project skeleton and the core calculation layer.

## Project status

Current phase: Foundation and calculation layer

Completed:
- Project structure and package layout
- SQLite schema for core data tables
- Core GE tax and profit calculations
- Minimal PySide6 application shell
- Test suite for key edge cases

## Planned next steps

1. Add live OSRS Wiki API integration
2. Implement stale price handling and local caching
3. Build the item search and dashboard views
4. Add recipe CRUD and scanning logic
5. Add historical charts and forecasting
6. Package for Linux distribution

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Tests

```bash
pytest -q
```
