from __future__ import annotations

import time
from typing import Any

import requests


class OSRSAPIError(RuntimeError):
    """Raised when the OSRS Wiki API fails or returns invalid data."""


class OSRSWikiClient:
    """Minimal client for the public OSRS Wiki price endpoints."""

    BASE_URL = "https://prices.runescape.wiki/api/v1/osrs"

    def __init__(
        self,
        user_agent: str = "OSRSProfitAdvisor/1.0 contact: moj-email@example.com",
        timeout: int = 15,
        max_retries: int = 3,
    ) -> None:
        self.user_agent = user_agent
        self.timeout = timeout
        self.max_retries = max_retries

    def _request_json(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"User-Agent": self.user_agent, "Accept": "application/json"}

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict):
                    raise ValueError("API response was not a JSON object")
                return payload
            except (requests.RequestException, ValueError, TypeError) as exc:
                if attempt == self.max_retries:
                    raise OSRSAPIError(f"Request failed for {endpoint}: {exc}") from exc
                time.sleep(attempt)

        raise OSRSAPIError(f"Request failed for {endpoint}: unknown error")

    def fetch_latest_prices(self) -> dict[str, Any]:
        return self._request_json("/latest")

    def fetch_mapping(self) -> dict[str, Any]:
        return self._request_json("/mapping")

    def fetch_timeseries(
        self,
        item_id: int,
        interval: str = "1h",
        start: int | None = None,
        end: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"id": item_id, "interval": interval}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return self._request_json("/timeseries", params=params)
