"""Edenic Cloud API client for Bluelab IntelliDose."""

import asyncio
import logging
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

    def __init__(self, api_token: str) -> None:
        self._headers = {"Authorization": api_token}

    async def _request(self, url: str) -> Any:
        """Make an authenticated GET request."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                if response.status == 401:
                    raise AuthError
                if response.status == 429:
                    raise RateLimitError
                response.raise_for_status()
                return await response.json()

    async def get_devices(self, organization_id: str) -> list[dict[str, Any]]:
        """Fetch device list for an organization."""
        return await self._request(f"{DEVICE_LIST_URL}{organization_id}")

    async def get_telemetry(self, device_id: str) -> dict[str, Any]:
        """Fetch latest telemetry for a single device."""
        return await self._request(f"{TELEMETRY_URL}{device_id}")

    async def get_device_attributes(self, device_id: str) -> dict[str, Any]:
        """Fetch device attributes (target setpoints)."""
        return await self._request(f"{DEVICE_ATTRIBUTE_URL}{device_id}")

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
