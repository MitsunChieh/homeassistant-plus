"""Sensor platform for Bluelab IntelliDose integration."""

import logging
from datetime import datetime, timezone
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BluelabAttributeCoordinator, BluelabTelemetryCoordinator
from .helpers import get_device_display_name

_LOGGER = logging.getLogger(__name__)

TELEMETRY_SENSOR_TYPES = [
    {
        "key": "ec",
        "name": "EC",
        "unit": "mS/cm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "ph",
        "name": "pH",
        "unit": "pH",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "nut_temp",
        "name": "Temperature",
        "unit": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
]

GATEWAY_SENSOR_TYPES = [
    {
        "key": "current_fw_version",
        "name": "Firmware Version",
        "entity_category": "diagnostic",
        "state_class": None,
    },
    {
        "key": "fw_state",
        "name": "Firmware State",
        "entity_category": "diagnostic",
        "state_class": None,
    },
    {
        "key": "eventsProduced",
        "name": "Events Produced",
        "entity_category": "diagnostic",
        "state_class": SensorStateClass.TOTAL_INCREASING,
    },
    {
        "key": "eventsSent",
        "name": "Events Sent",
        "entity_category": "diagnostic",
        "state_class": SensorStateClass.TOTAL_INCREASING,
    },
    {
        "key": "customconnectorEventsProduced",
        "name": "Custom Connector Events Produced",
        "entity_category": "diagnostic",
        "state_class": SensorStateClass.TOTAL_INCREASING,
    },
    {
        "key": "customconnectorEventsSent",
        "name": "Custom Connector Events Sent",
        "entity_category": "diagnostic",
        "state_class": SensorStateClass.TOTAL_INCREASING,
    },
]

ATTRIBUTE_SENSOR_TYPES = [
    {
        "key": "setting.ec_set_point",
        "name": "EC Target",
        "unit": "mS/cm",
        "device_class": None,
        "state_class": None,
    },
    {
        "key": "setting.ph_set_point",
        "name": "pH Target",
        "unit": "pH",
        "device_class": None,
        "state_class": None,
    },
]


def make_unique_id(device_id: str, sensor_key: str) -> str:
    """Generate unique_id from device ID and sensor key."""
    return f"{DOMAIN}_{device_id}_{sensor_key}"


def format_telemetry_timestamp(ts_ms: int | None) -> str | None:
    """Convert ms epoch to ISO 8601 UTC string, or None if not available."""
    if ts_ms is None:
        return None
    dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
    return dt.isoformat(timespec="seconds")


def make_device_info(device_id: str, device_name: str, model: str = "IntelliDose") -> dict[str, Any]:
    """Generate HA device info dict for a Bluelab device."""
    return {
        "identifiers": {(DOMAIN, device_id)},
        "name": device_name,
        "manufacturer": "Bluelab",
        "model": model,
    }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bluelab sensor entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    gateways: list[dict[str, Any]] = data["gateways"]
    intellidose: list[dict[str, Any]] = data["intellidose"]
    telemetry_coordinator: BluelabTelemetryCoordinator = data["telemetry_coordinator"]
    attribute_coordinator: BluelabAttributeCoordinator = data["attribute_coordinator"]

    entities: list[SensorEntity] = []

    for device in intellidose:
        device_id = device["id"]
        device_name = get_device_display_name(device)

        for sensor_type in TELEMETRY_SENSOR_TYPES:
            entities.append(
                BluelabTelemetrySensor(
                    coordinator=telemetry_coordinator,
                    device_id=device_id,
                    device_name=device_name,
                    sensor_type=sensor_type,
                )
            )

        for sensor_type in ATTRIBUTE_SENSOR_TYPES:
            entities.append(
                BluelabAttributeSensor(
                    coordinator=attribute_coordinator,
                    device_id=device_id,
                    device_name=device_name,
                    sensor_type=sensor_type,
                )
            )

    for device in gateways:
        device_id = device["id"]
        device_name = get_device_display_name(device)

        for sensor_type in GATEWAY_SENSOR_TYPES:
            entities.append(
                BluelabGatewayDiagnosticSensor(
                    coordinator=telemetry_coordinator,
                    device_id=device_id,
                    device_name=device_name,
                    sensor_type=sensor_type,
                )
            )

    async_add_entities(entities)


class BluelabTelemetrySensor(CoordinatorEntity, SensorEntity):
    """Sensor entity for IntelliDose telemetry readings."""

    def __init__(
        self,
        coordinator: BluelabTelemetryCoordinator,
        device_id: str,
        device_name: str,
        sensor_type: dict[str, Any],
    ) -> None:
        super().__init__(coordinator)
        self._device_id = device_id
        self._sensor_key = sensor_type["key"]
        self._attr_unique_id = make_unique_id(device_id, self._sensor_key)
        self._attr_name = f"{device_name} {sensor_type['name']}"
        self._attr_native_unit_of_measurement = sensor_type["unit"]
        self._attr_device_class = sensor_type["device_class"]
        self._attr_state_class = sensor_type["state_class"]
        self._attr_device_info = make_device_info(device_id, device_name)

    @property
    def native_value(self) -> float | None:
        """Return the sensor value from coordinator data."""
        if self.coordinator.data is None:
            return None
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return None
        return device_data.get(self._sensor_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra state attributes including last_reading timestamp."""
        if self.coordinator.data is None:
            return None
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return None
        ts = format_telemetry_timestamp(device_data.get("_ts"))
        if ts is None:
            return None
        return {"last_reading": ts}

    @property
    def available(self) -> bool:
        """Return True if device has data in the coordinator."""
        if not super().available:
            return False
        if self.coordinator.data is None:
            return False
        return self._device_id in self.coordinator.data


class BluelabAttributeSensor(CoordinatorEntity, SensorEntity):
    """Sensor entity for IntelliDose target setpoints."""

    def __init__(
        self,
        coordinator: BluelabAttributeCoordinator,
        device_id: str,
        device_name: str,
        sensor_type: dict[str, Any],
    ) -> None:
        super().__init__(coordinator)
        self._device_id = device_id
        self._sensor_key = sensor_type["key"]
        self._attr_unique_id = make_unique_id(device_id, self._sensor_key)
        self._attr_name = f"{device_name} {sensor_type['name']}"
        self._attr_native_unit_of_measurement = sensor_type["unit"]
        self._attr_device_class = sensor_type["device_class"]
        self._attr_state_class = sensor_type["state_class"]
        self._attr_device_info = make_device_info(device_id, device_name)

    @property
    def native_value(self) -> float | None:
        """Return the target setpoint from coordinator data."""
        if self.coordinator.data is None:
            return None
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return None
        return device_data.get(self._sensor_key)


class BluelabGatewayDiagnosticSensor(CoordinatorEntity, SensorEntity):
    """Sensor entity for IntelliLink gateway diagnostic telemetry."""

    def __init__(
        self,
        coordinator: BluelabTelemetryCoordinator,
        device_id: str,
        device_name: str,
        sensor_type: dict[str, Any],
    ) -> None:
        super().__init__(coordinator)
        self._device_id = device_id
        self._sensor_key = sensor_type["key"]
        self._attr_unique_id = make_unique_id(device_id, self._sensor_key)
        self._attr_name = f"{device_name} {sensor_type['name']}"
        self._attr_entity_category = sensor_type["entity_category"]
        self._attr_state_class = sensor_type.get("state_class")
        self._attr_device_info = make_device_info(device_id, device_name, model="IntelliLink")

    @property
    def native_value(self) -> str | float | None:
        """Return the diagnostic value from coordinator data."""
        if self.coordinator.data is None:
            return None
        device_data = self.coordinator.data.get(self._device_id)
        if device_data is None:
            return None
        return device_data.get(self._sensor_key)

    @property
    def available(self) -> bool:
        """Return True if device has data in the coordinator."""
        if not super().available:
            return False
        if self.coordinator.data is None:
            return False
        return self._device_id in self.coordinator.data
