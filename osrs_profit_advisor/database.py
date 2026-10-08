from __future__ import annotations

import sqlite3
from pathlib import Path

from osrs_profit_advisor.config import get_default_db_path


def initialize_database(db_path: str | Path | None = None) -> str:
    db_file = Path(db_path) if db_path else get_default_db_path()
    db_file.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(db_file))
    connection.execute("PRAGMA journal_mode=WAL;")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            members INTEGER DEFAULT 0,
            lowalch INTEGER,
            highalch INTEGER,
            limit INTEGER,
            examine TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS current_prices (
            item_id INTEGER PRIMARY KEY,
            high_price INTEGER,
            low_price INTEGER,
            avg_price INTEGER,
            volume INTEGER,
            buy_limit INTEGER,
            last_updated TEXT,
            is_stale INTEGER DEFAULT 0,
            raw_json TEXT,
            FOREIGN KEY(item_id) REFERENCES items(id)
        );
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            captured_at TEXT NOT NULL,
            high_price INTEGER,
            low_price INTEGER,
            avg_price INTEGER,
            volume INTEGER,
            FOREIGN KEY(item_id) REFERENCES items(id)
        );
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            output_item_id INTEGER NOT NULL,
            output_quantity INTEGER NOT NULL,
            craft_time_seconds INTEGER DEFAULT 0,
            required_skill TEXT,
            required_level INTEGER,
            failure_chance REAL DEFAULT 0,
            extra_costs REAL DEFAULT 0,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS recipe_inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(recipe_id) REFERENCES recipes(id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        );
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS recipe_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(recipe_id) REFERENCES recipes(id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        );
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL,
            message TEXT,
            item_count INTEGER DEFAULT 0,
            started_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    connection.commit()
    connection.close()
    return str(db_file)
