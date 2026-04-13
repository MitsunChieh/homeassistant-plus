"""Bluelab IntelliDose integration for Home Assistant."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import EdenicApiClient
from .config_flow import validate_credentials
from .const import CONF_API_TOKEN, CONF_ORGANIZATION_ID, DOMAIN
from .coordinator import BluelabAttributeCoordinator, BluelabTelemetryCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bluelab IntelliDose from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    api_token = entry.data[CONF_API_TOKEN]
    organization_id = entry.data[CONF_ORGANIZATION_ID]

    client = EdenicApiClient(api_token)
    devices = await client.get_devices(organization_id)
    device_ids = [d["id"] for d in devices]

    telemetry_coordinator = BluelabTelemetryCoordinator(hass, client, device_ids)
    attribute_coordinator = BluelabAttributeCoordinator(hass, client, device_ids)

    await telemetry_coordinator.async_config_entry_first_refresh()
    await attribute_coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "devices": devices,
        "telemetry_coordinator": telemetry_coordinator,
        "attribute_coordinator": attribute_coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
