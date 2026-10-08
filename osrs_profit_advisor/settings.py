from __future__ import annotations

from pathlib import Path

from osrs_profit_advisor.config import DEFAULT_CONFIG, get_default_db_path
from osrs_profit_advisor.database import initialize_database


def load_settings() -> dict:
    return DEFAULT_CONFIG.copy()


def ensure_database() -> Path:
    db_path = get_default_db_path()
    initialize_database(db_path)
    return db_path
