"""Edenic Cloud API client for Bluelab IntelliDose."""

import asyncio
import logging
from urllib.parse import quote
from typing import Any

import aiohttp

from .const import (
    DEVICE_ATTRIBUTE_URL,
    DEVICE_LIST_URL,
    INTER_DEVICE_DELAY,
    TELEMETRY_URL,
)

_LOGGER = logging.getLogger(__name__)


class AuthError(Exception):
    """Raised when API authentication fails (HTTP 401)."""


class RateLimitError(Exception):
    """Raised when API rate limit is hit (HTTP 429)."""


class ApiError(Exception):
    """Raised for other API errors."""


class EdenicApiClient:
    """Client for the Edenic Cloud API."""

    def __init__(self, api_token: str, session: aiohttp.ClientSession | None = None) -> None:
        self._headers = {"Authorization": api_token}
        self._session = session
        self._owns_session = session is None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Return the shared session, creating one if needed."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
            self._owns_session = True
        return self._session

    async def close(self) -> None:
        """Close the session if we own it."""
        if self._owns_session and self._session and not self._session.closed:
            await self._session.close()

    async def _request(self, url: str) -> Any:
        """Make an authenticated GET request."""
        session = await self._get_session()
        async with session.get(url, headers=self._headers) as response:
            if response.status == 401:
                raise AuthError
            if response.status == 429:
                raise RateLimitError
            response.raise_for_status()
            return await response.json()

    async def get_devices(self, organization_id: str) -> list[dict[str, Any]]:
        """Fetch device list for an organization."""
        return await self._request(f"{DEVICE_LIST_URL}{quote(organization_id, safe='')}")

    async def get_telemetry(self, device_id: str) -> dict[str, Any]:
        """Fetch latest telemetry for a single device.

        Raw API format: {"ph": [{"ts": ..., "value": "6.81"}], ...}
        Returns normalized: {"ph": 6.81, "ec": 1.98, "nut_temp": 22.89}
        """
        raw = await self._request(f"{TELEMETRY_URL}{quote(device_id, safe='')}")
        return self._normalize_telemetry(raw)

    @staticmethod
    def _normalize_telemetry(raw: dict[str, Any]) -> dict[str, Any]:
        """Convert API telemetry format to flat dict.

        Numeric strings are converted to float; non-numeric strings are kept as-is.
        Also extracts the most recent timestamp as "_ts" (ms epoch).
        """
        result: dict[str, Any] = {}
        latest_ts: int | None = None
        for key, entries in raw.items():
            if isinstance(entries, list) and entries:
                try:
                    raw_value = entries[0]["value"]
                    try:
                        result[key] = float(raw_value)
                    except (ValueError, TypeError):
                        result[key] = raw_value
                    ts = entries[0].get("ts")
                    if ts is not None and (latest_ts is None or ts > latest_ts):
                        latest_ts = ts
                except (KeyError, IndexError):
                    result[key] = None
        if latest_ts is not None:
            result["_ts"] = latest_ts
        return result

    async def get_device_attributes(self, device_id: str) -> dict[str, Any]:
        """Fetch device attributes (target setpoints).

        Raw API format: [{"key": "setting.ec_set_point", "value": {"value": 2.2, ...}}, ...]
        Returns normalized: {"setting.ec_set_point": 2.2, "setting.ph_set_point": 5.4}
        """
        raw = await self._request(f"{DEVICE_ATTRIBUTE_URL}{quote(device_id, safe='')}")
        return self._normalize_attributes(raw)

    @staticmethod
    def _normalize_attributes(raw: list[dict[str, Any]]) -> dict[str, Any]:
        """Convert API attribute list to flat key->value dict."""
        result: dict[str, Any] = {}
        for item in raw:
            key = item.get("key", "")
            value = item.get("value")
            if isinstance(value, dict) and "value" in value:
                result[key] = value["value"]
            elif value is not None:
                result[key] = value
        return result

    async def get_telemetry_all_devices(
        self,
        device_ids: list[str],
        inter_device_delay: float = INTER_DEVICE_DELAY,
    ) -> dict[str, dict[str, Any]]:
        """Fetch telemetry for all devices with inter-device delay.

        Returns a dict mapping device_id to telemetry data.
        Devices that fail are logged and skipped.
        """
        results: dict[str, dict[str, Any]] = {}
        for i, device_id in enumerate(device_ids):
            if i > 0:
                await asyncio.sleep(inter_device_delay)
            try:
                results[device_id] = await self.get_telemetry(device_id)
            except RateLimitError:
                _LOGGER.warning(
                    "Rate limited fetching telemetry for device %s", device_id
                )
                raise
            except Exception:
                _LOGGER.warning(
                    "Failed to fetch telemetry for device %s", device_id,
                    exc_info=True,
                )
        return results
