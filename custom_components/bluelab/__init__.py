"""Bluelab IntelliDose integration for Home Assistant."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import EdenicApiClient
from .const import CONF_API_TOKEN, CONF_ORGANIZATION_ID, DOMAIN
from .coordinator import BluelabAttributeCoordinator, BluelabTelemetryCoordinator
from .helpers import classify_devices

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bluelab IntelliDose from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    api_token = entry.data[CONF_API_TOKEN]
    organization_id = entry.data[CONF_ORGANIZATION_ID]

    client = EdenicApiClient(api_token)
    all_devices = await client.get_devices(organization_id)
    gateways, intellidose = classify_devices(all_devices)
    all_device_ids = [d["id"] for d in gateways + intellidose]
    intellidose_device_ids = [d["id"] for d in intellidose]

    telemetry_coordinator = BluelabTelemetryCoordinator(hass, client, all_device_ids)
    attribute_coordinator = BluelabAttributeCoordinator(hass, client, intellidose_device_ids)

    await telemetry_coordinator.async_config_entry_first_refresh()
    await attribute_coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "gateways": gateways,
        "intellidose": intellidose,
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
