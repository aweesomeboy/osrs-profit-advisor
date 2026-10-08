from __future__ import annotations

import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from osrs_profit_advisor.calculations import is_data_stale
from osrs_profit_advisor.services.osrs_api import OSRSWikiClient


class SyncService:
    """Syncs public price data from the OSRS Wiki into the local SQLite database."""

    def __init__(self, database_path: str | Path, client: OSRSWikiClient | None = None) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.client = client or OSRSWikiClient()
        self.connection = sqlite3.connect(str(self.database_path))
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _normalise_item_payload(self, item_payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(item_payload.get("id") or item_payload.get("item_id") or 0),
            "name": str(item_payload.get("name") or item_payload.get("itemName") or "Unknown"),
            "high_price": item_payload.get("high_price") or item_payload.get("high") or item_payload.get("highPrice"),
            "low_price": item_payload.get("low_price") or item_payload.get("low") or item_payload.get("lowPrice"),
            "avg_price": item_payload.get("avg_price") or item_payload.get("avg") or item_payload.get("average"),
            "volume": item_payload.get("volume") or item_payload.get("qty") or item_payload.get("trading_volume"),
            "buy_limit": item_payload.get("buy_limit") or item_payload.get("limit") or item_payload.get("buyLimit"),
            "last_updated": item_payload.get("timestamp") or item_payload.get("last_updated") or self._now_iso(),
        }

    def _save_item(self, item: dict[str, Any]) -> None:
        item_id = item["id"]
        if item_id <= 0:
            return

        self.connection.execute(
            """
            INSERT INTO items (id, name, limit, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                limit = excluded.limit,
                updated_at = CURRENT_TIMESTAMP
            """,
            (item_id, item["name"], item["buy_limit"]),
        )

        self.connection.execute(
            """
            INSERT INTO current_prices (item_id, high_price, low_price, avg_price, volume, buy_limit, last_updated, is_stale, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(item_id) DO UPDATE SET
                high_price = excluded.high_price,
                low_price = excluded.low_price,
                avg_price = excluded.avg_price,
                volume = excluded.volume,
                buy_limit = excluded.buy_limit,
                last_updated = excluded.last_updated,
                is_stale = excluded.is_stale,
                raw_json = excluded.raw_json
            """,
            (
                item_id,
                item["high_price"],
                item["low_price"],
                item["avg_price"],
                item["volume"],
                item["buy_limit"],
                item["last_updated"],
                int(is_data_stale(item["last_updated"], max_age_seconds=1800)),
                str(item),
            ),
        )

        self.connection.execute(
            """
            INSERT INTO price_history (item_id, captured_at, high_price, low_price, avg_price, volume)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item_id,
                item["last_updated"] or self._now_iso(),
                item["high_price"],
                item["low_price"],
                item["avg_price"],
                item["volume"],
            ),
        )

    def sync_latest_prices(self) -> dict[str, Any]:
        start_time = time.time()
        latest = self.client.fetch_latest_prices()
        mapping = self.client.fetch_mapping()

        item_names: dict[int, str] = {}
        if isinstance(mapping, dict):
            for entry in mapping.get("data", []) or mapping.get("items", []) or []:
                if isinstance(entry, dict):
                    item_id = entry.get("id") or entry.get("item_id")
                    if item_id is not None:
                        item_names[int(item_id)] = str(entry.get("name") or entry.get("itemName") or "Unknown")

        latest_data = latest.get("data", []) if isinstance(latest, dict) else []
        if not isinstance(latest_data, list):
            latest_data = []

        count = 0
        for raw_item in latest_data:
            if not isinstance(raw_item, dict):
                continue
            item = self._normalise_item_payload(raw_item)
            if item["name"] == "Unknown" and item["id"] in item_names:
                item["name"] = item_names[item["id"]]
            self._save_item(item)
            count += 1

        self.connection.execute(
            "INSERT INTO sync_log (status, message, item_count, started_at, completed_at) VALUES (?, ?, ?, ?, ?)",
            (
                "success",
                f"Synced {count} items in {time.time() - start_time:.2f}s",
                count,
                self._now_iso(),
                self._now_iso(),
            ),
        )
        self.connection.commit()
        return {"item_count": count, "synced_at": self._now_iso()}

    def sync_timeseries(self, item_id: int, interval: str = "1h") -> list[dict[str, Any]]:
        payload = self.client.fetch_timeseries(item_id=item_id, interval=interval)
        data = payload.get("data", []) if isinstance(payload, dict) else []
        rows: list[dict[str, Any]] = []
        for point in data:
            if isinstance(point, dict):
                rows.append({
                    "timestamp": point.get("timestamp") or point.get("time") or self._now_iso(),
                    "high": point.get("high") or point.get("high_price"),
                    "low": point.get("low") or point.get("low_price"),
                    "avg": point.get("avg") or point.get("avg_price"),
                    "volume": point.get("volume"),
                })
        return rows
