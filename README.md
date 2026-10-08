# OSRS Profit Advisor

OSRS Profit Advisor is a modular Linux desktop application built with Python and PySide6 for tracking Old School RuneScape Grand Exchange prices, analyzing profit opportunities, and forecasting short-term market movements.

This project is structured so it can be extended gradually without breaking the application. The early implementation includes the data layer, calculation helpers, API integration, recipe storage, and a working PySide6 tabbed interface scaffold.

## Features included in this version

- Local SQLite database for price snapshots, history, recipes, settings, and sync logs
- OSRS Wiki API client using a custom User-Agent
- Stale-price checks and validation for malformed API responses
- Core GE tax and profit calculations
- Recipe persistence with JSON import/export support
- Modular PySide6 desktop UI shell with tabs for dashboard, item search, recipes, forecast, and settings
- Test suite for calculations and common edge cases

## Project structure

```text
osrs-profit-advisor/
├── data/
│   ├── recipes.json
│   └── .gitkeep
├── docs/
│   ├── linux_run.md
│   ├── appimage.md
│   ├── deb_package.md
│   └── adding_recipes.md
├── osrs_profit_advisor/
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py
│   ├── calculations.py
│   ├── config.py
│   ├── database.py
│   ├── forecast.py
│   ├── models.py
│   ├── recipe_manager.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── osrs_api.py
│   │   └── sync_service.py
│   └── ui/
│       ├── __init__.py
│       └── main_window.py
├── tests/
│   ├── test_calculations.py
│   └── test_recipe_manager.py
├── .gitignore
├── README.md
├── config.yaml.example
├── requirements.txt
├── run.py
└── LICENSE
```

## Requirements

- Python 3.10+
- PySide6
- requests
- PyYAML
- pytest

## Quick start on Linux

```bash
git clone https://github.com/aweesomeboy/osrs-profit-advisor.git
cd osrs-profit-advisor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## How to use it

1. Launch the app with `python run.py`.
2. On first run, the application initializes the SQLite database in the `data` folder.
3. Use the Dashboard tab to inspect the latest status and sync state.
4. Open Item Search to browse live market data and search by item name.
5. Open Recipe Scanner to view recipe profitability and filters.
6. Use Price Forecast to review short-term trend estimates and confidence warnings.
7. Open Settings to configure database location, data refresh interval, and API timeout settings.

## Configuration

A sample configuration file is provided at `config.yaml.example`.

```yaml
database:
  path: "data/osrs_profit_advisor.db"
  sync_interval_minutes: 5
api:
  user_agent: "OSRSProfitAdvisor/1.0 contact: moj-email@example.com"
  timeout_seconds: 15
  max_retries: 3
ui:
  window_title: "OSRS Profit Advisor"
  refresh_interval_ms: 300000
```

The app reads configuration settings from a local YAML file when available, and the defaults are defined in `osrs_profit_advisor/config.py`.

## Recipe data format

Recipe definitions can be stored in JSON and imported into the app. Example:

```json
[
  {
    "name": "Cooked Karambwan",
    "inputs": [
      {"item_id": 3142, "quantity": 1},
      {"item_id": 3150, "quantity": 1}
    ],
    "output_item_id": 3144,
    "output_quantity": 1,
    "craft_time_seconds": 60,
    "required_skill": "Cooking",
    "required_level": 30,
    "failure_chance": 0.0,
    "extra_costs": 0,
    "notes": "Example recipe"
  }
]
```

A sample file is provided in `data/recipes.json`.

## Documentation

The project includes Linux packaging and usage docs in `docs/`:

- `docs/linux_run.md` — Linux installation and execution instructions
- `docs/appimage.md` — AppImage build steps
- `docs/deb_package.md` — `.deb` packaging instructions
- `docs/adding_recipes.md` — how to add or edit recipes in the app and JSON file

## Safety and scope

This application is informational only. It does not:

- automate clicking in-game,
- bot or automate market actions,
- control RuneLite,
- send commands to the game,
- place automatic buy/sell orders.

It only retrieves public market information and calculates estimates.

## Development notes

The project is intentionally modular so future features can be added without rewriting the app:

- data access layer: database and API integration
- calculation layer: GE tax, profit, ROI, price forecasts
- business logic: recipe management and filtering
- UI layer: PySide6 tabbed screens
- packaging assistance: Linux distribution docs

## Running tests

```bash
pytest -q
```

## License

This project is distributed under the MIT license.
