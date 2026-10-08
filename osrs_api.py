import asyncio
from datetime import datetime
from typing import Optional

import httpx

LATEST_URL = "https://prices.runescape.wiki/api/v1/osrs/latest"
MAPPING_URL = "https://prices.runescape.wiki/api/v1/osrs/mapping"
USER_AGENT = "OSRSProfitAdvisor/1.0 contact: your-email@example.com"
TIMEOUT = 30.0


class OSRSAPIManager:
    def __init__(self):
        self.items_cache = {}
        self.last_sync = None
        self.next_sync = None
        self.error = None
        self.sync_interval = 300

    async def _get_json(self, url: str):
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                response = await client.get(url, headers={"User-Agent": USER_AGENT})
                response.raise_for_status()
                return response.json()
        except Exception as exc:
            self.error = str(exc)
            return None

    async def refresh_data(self):
        self.error = None
        latest_payload = await self._get_json(LATEST_URL)
        mapping_payload = await self._get_json(MAPPING_URL)

        if latest_payload is None or mapping_payload is None:
            raise RuntimeError(self.error or "Failed to fetch OSRS Wiki data")

        latest_data = latest_payload.get("data", {})
        mapping_data = mapping_payload.get("data", {})

        if isinstance(mapping_data, list):
            normalized_mapping = {}
            for entry in mapping_data:
                item_id = entry.get("id")
                if item_id is not None:
                    normalized_mapping[str(item_id)] = entry
            mapping_data = normalized_mapping

        self.items_cache = {}
        now_iso = datetime.now().isoformat()

        for item_id_str, item_info in latest_data.items():
            try:
                item_id = int(item_id_str)
            except (TypeError, ValueError):
                continue

            entry = mapping_data.get(str(item_id), {}) if isinstance(mapping_data, dict) else {}
            name = entry.get("name") or f"Item {item_id}"
            buy_limit = entry.get("limit")
            high_price = item_info.get("high")
            low_price = item_info.get("low")
            high_time = item_info.get("highTime")
            low_time = item_info.get("lowTime")

            margin = None
            roi = None
            if high_price is not None and low_price is not None:
                margin = high_price - low_price
                if low_price > 0:
                    roi = (margin / low_price) * 100

            self.items_cache[item_id] = {
                "item_id": item_id,
                "name": name,
                "high_price": high_price,
                "low_price": low_price,
                "margin": margin,
                "roi": roi,
                "high_time": high_time,
                "low_time": low_time,
                "buy_limit": buy_limit,
                "timestamp": now_iso,
                "last_update": now_iso,
            }

        self.last_sync = now_iso
        self.next_sync = datetime.now().timestamp() + self.sync_interval

    def get_items(
        self,
        search: Optional[str] = None,
        sort_by: str = "name",
        sort_order: str = "asc",
        page: int = 1,
        page_size: int = 20,
    ):
        items = list(self.items_cache.values())

        if search:
            needle = search.lower()
            items = [
                item
                for item in items
                if needle in str(item["item_id"]).lower() or needle in item["name"].lower()
            ]

        valid_sort_fields = {
            "name",
            "item_id",
            "high_price",
            "low_price",
            "margin",
            "roi",
            "buy_limit",
            "timestamp",
        }
        sort_key = sort_by if sort_by in valid_sort_fields else "name"

        def item_sort_value(item):
            value = item.get(sort_key)
            if value is None:
                return -999999999
            if isinstance(value, str):
                return value.lower()
            return value

        items = sorted(items, key=item_sort_value, reverse=(sort_order == "desc"))

        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        page_items = items[start:end]

        return {
            "items": page_items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size) if total else 1,
        }

    def get_item(self, item_id: int):
        return self.items_cache.get(item_id)

    def get_health(self):
        stale = False
        if self.last_sync:
            last_sync_dt = datetime.fromisoformat(self.last_sync)
            stale = (datetime.now() - last_sync_dt).total_seconds() > self.sync_interval * 1.5

        return {
            "status": "error" if self.error else "ok",
            "last_sync": self.last_sync,
            "next_sync": datetime.fromtimestamp(self.next_sync).isoformat() if self.next_sync else None,
            "item_count": len(self.items_cache),
            "stale": stale,
            "error": self.error,
        }
