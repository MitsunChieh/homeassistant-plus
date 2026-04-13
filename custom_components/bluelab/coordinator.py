"""Data update coordinators for Bluelab IntelliDose."""

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import EdenicApiClient, RateLimitError
from .const import (
    DOMAIN,
    INTER_DEVICE_DELAY,
    TELEMETRY_UPDATE_INTERVAL,
    ATTRIBUTE_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class BluelabTelemetryCoordinator(DataUpdateCoordinator[dict[str, dict[str, Any]]]):
    """Coordinator that polls telemetry for all IntelliDose devices."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: EdenicApiClient,
        device_ids: list[str],
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_telemetry",
            update_interval=TELEMETRY_UPDATE_INTERVAL,
        )
        self._client = client
        self._device_ids = device_ids

    async def _async_update_data(self) -> dict[str, dict[str, Any]]:
        """Fetch telemetry for all devices with inter-device delay."""
        try:
            return await self._client.get_telemetry_all_devices(
                self._device_ids,
                inter_device_delay=INTER_DEVICE_DELAY,
            )
        except RateLimitError as err:
            _LOGGER.warning("Edenic API rate limited, will retry next interval")
            # Return previous data instead of failing
            if self.data is not None:
                return self.data
            raise UpdateFailed("Rate limited by Edenic API") from err
        except Exception as err:
            raise UpdateFailed(f"Error fetching telemetry: {err}") from err


class BluelabAttributeCoordinator(DataUpdateCoordinator[dict[str, dict[str, Any]]]):
    """Coordinator that polls device attributes for all IntelliDose devices."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: EdenicApiClient,
        device_ids: list[str],
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_attributes",
            update_interval=ATTRIBUTE_UPDATE_INTERVAL,
        )
        self._client = client
        self._device_ids = device_ids

    async def _async_update_data(self) -> dict[str, dict[str, Any]]:
        """Fetch device attributes for all devices."""
        results: dict[str, dict[str, Any]] = {}
        for device_id in self._device_ids:
            try:
                results[device_id] = await self._client.get_device_attributes(
                    device_id
                )
            except Exception:
                _LOGGER.warning(
                    "Failed to fetch attributes for device %s",
                    device_id,
                    exc_info=True,
                )
        if not results and self.data is not None:
            return self.data
        return results
