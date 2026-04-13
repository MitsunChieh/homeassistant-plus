"""Sensor platform for Bluelab IntelliDose integration."""

import logging
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
        "key": "temperature",
        "name": "Temperature",
        "unit": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
]

ATTRIBUTE_SENSOR_TYPES = [
    {
        "key": "ec_target",
        "name": "EC Target",
        "unit": "mS/cm",
        "device_class": None,
        "state_class": None,
    },
    {
        "key": "ph_target",
        "name": "pH Target",
        "unit": "pH",
        "device_class": None,
        "state_class": None,
    },
]


def make_unique_id(device_id: str, sensor_key: str) -> str:
    """Generate unique_id from device ID and sensor key."""
    return f"{DOMAIN}_{device_id}_{sensor_key}"


def make_device_info(device_id: str, device_name: str) -> dict[str, Any]:
    """Generate HA device info dict for an IntelliDose device."""
    return {
        "identifiers": {(DOMAIN, device_id)},
        "name": device_name,
        "manufacturer": "Bluelab",
        "model": "IntelliDose",
    }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bluelab sensor entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    devices: list[dict[str, Any]] = data["devices"]
    telemetry_coordinator: BluelabTelemetryCoordinator = data["telemetry_coordinator"]
    attribute_coordinator: BluelabAttributeCoordinator = data["attribute_coordinator"]

    entities: list[SensorEntity] = []

    for device in devices:
        device_id = device["id"]
        device_name = device.get("name", device_id)

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
