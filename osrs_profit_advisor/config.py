from __future__ import annotations

from pathlib import Path
import os

DEFAULT_CONFIG = {
    "database": {"path": "data/osrs_profit_advisor.db", "sync_interval_minutes": 5},
    "api": {"user_agent": "OSRSProfitAdvisor/1.0 contact: moj-email@example.com", "timeout_seconds": 15, "max_retries": 3},
    "ui": {"window_title": "OSRS Profit Advisor", "refresh_interval_ms": 300000},
}


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_default_db_path() -> Path:
    root = get_project_root()
    db_path = root / DEFAULT_CONFIG["database"]["path"]
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_default_config() -> dict:
    return DEFAULT_CONFIG.copy()
