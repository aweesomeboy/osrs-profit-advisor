# OSRS Profit Advisor

A Linux desktop application for tracking Old School RuneScape Grand Exchange prices, recipe profitability, and price forecasting.

This repository is being built incrementally. The current milestone adds the live API client and the SQLite synchronization layer.

## Current status

Completed:
- Project structure and package layout
- SQLite schema for core data tables
- Core GE tax and profit calculations
- Minimal PySide6 application shell
- Initial unit tests for calculations and edge cases
- Live OSRS Wiki API client
- Local synchronization service for latest prices and time-series data

## Planned next steps

1. Build the item search and dashboard views
2. Add recipe CRUD, import/export, and filtering
3. Implement historical charts and simple forecasting
4. Package the app for Linux
5. Finalize documentation and release prep

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
