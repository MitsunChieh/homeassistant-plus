"""Tests for Bluelab IntelliDose sensor entities."""

import pytest

from custom_components.bluelab.const import DOMAIN


MOCK_DEVICES = [
    {"id": "dev-1", "name": "IDose1", "type": "intellidose"},
    {"id": "dev-2", "name": "IDose2", "type": "intellidose"},
    {"id": "dev-3", "name": "IDose3", "type": "intellidose"},
]

MOCK_TELEMETRY = {
    "dev-1": {"ec": 1.2, "ph": 7.0, "temperature": 21.0},
    "dev-2": {"ec": 1.1, "ph": 6.7, "temperature": 20.0},
    "dev-3": {"ec": 1.9, "ph": 6.1, "temperature": 22.0},
}

MOCK_ATTRIBUTES = {
    "dev-1": {"ec_target": 2.2, "ph_target": 5.4},
    "dev-2": {"ec_target": 1.0, "ph_target": 5.8},
    "dev-3": {"ec_target": 1.0, "ph_target": 6.0},
}


class TestSensorDescriptions:
    """Test sensor entity creation logic."""

    def test_three_devices_create_nine_telemetry_sensors(self):
        """3 devices × 3 sensors (EC, pH, temp) = 9 telemetry entities."""
        from custom_components.bluelab.sensor import TELEMETRY_SENSOR_TYPES

        total = len(MOCK_DEVICES) * len(TELEMETRY_SENSOR_TYPES)
        assert total == 9

    def test_three_devices_create_six_target_sensors(self):
        """3 devices × 2 targets (EC target, pH target) = 6 target entities."""
        from custom_components.bluelab.sensor import ATTRIBUTE_SENSOR_TYPES

        total = len(MOCK_DEVICES) * len(ATTRIBUTE_SENSOR_TYPES)
        assert total == 6

    def test_telemetry_sensor_types_have_required_fields(self):
        """Each telemetry sensor type has key, name, unit, and state_class."""
        from custom_components.bluelab.sensor import TELEMETRY_SENSOR_TYPES

        for sensor_type in TELEMETRY_SENSOR_TYPES:
            assert "key" in sensor_type
            assert "name" in sensor_type
            assert "unit" in sensor_type
            assert "state_class" in sensor_type

    def test_ec_sensor_unit(self):
        """EC sensor uses mS/cm unit."""
        from custom_components.bluelab.sensor import TELEMETRY_SENSOR_TYPES

        ec = next(s for s in TELEMETRY_SENSOR_TYPES if s["key"] == "ec")
        assert ec["unit"] == "mS/cm"

    def test_ph_sensor_unit(self):
        """pH sensor uses pH unit."""
        from custom_components.bluelab.sensor import TELEMETRY_SENSOR_TYPES

        ph = next(s for s in TELEMETRY_SENSOR_TYPES if s["key"] == "ph")
        assert ph["unit"] == "pH"

    def test_temperature_sensor_has_device_class(self):
        """Temperature sensor has device_class temperature."""
        from custom_components.bluelab.sensor import TELEMETRY_SENSOR_TYPES

        temp = next(s for s in TELEMETRY_SENSOR_TYPES if s["key"] == "temperature")
        assert temp.get("device_class") == "temperature"
        assert temp["unit"] == "°C"

    def test_unique_id_format(self):
        """Entity unique_id is derived from device ID and sensor key."""
        from custom_components.bluelab.sensor import make_unique_id

        uid = make_unique_id("dev-1", "ec")
        assert uid == f"{DOMAIN}_dev-1_ec"

    def test_device_info(self):
        """Device info has manufacturer Bluelab and model IntelliDose."""
        from custom_components.bluelab.sensor import make_device_info

        info = make_device_info("dev-1", "IDose1")
        assert info["manufacturer"] == "Bluelab"
        assert info["model"] == "IntelliDose"
        assert info["name"] == "IDose1"
        assert ("bluelab", "dev-1") in info["identifiers"]
