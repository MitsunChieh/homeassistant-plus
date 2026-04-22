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

        temp = next(s for s in TELEMETRY_SENSOR_TYPES if s["key"] == "nut_temp")
        assert temp.get("device_class") == "temperature"
        assert temp["unit"] == "°C"

    def test_unique_id_format(self):
        """Entity unique_id is derived from device ID and sensor key."""
        from custom_components.bluelab.sensor import make_unique_id

        uid = make_unique_id("dev-1", "ec")
        assert uid == f"{DOMAIN}_dev-1_ec"

    def test_device_info_intellidose(self):
        """IntelliDose device info has model IntelliDose."""
        from custom_components.bluelab.sensor import make_device_info

        info = make_device_info("dev-1", "IDose A", model="IntelliDose")
        assert info["manufacturer"] == "Bluelab"
        assert info["model"] == "IntelliDose"
        assert info["name"] == "IDose A"
        assert ("bluelab", "dev-1") in info["identifiers"]

    def test_device_info_gateway(self):
        """Gateway device info has model IntelliLink."""
        from custom_components.bluelab.sensor import make_device_info

        info = make_device_info("gw-1", "Bluelab-AABE", model="IntelliLink")
        assert info["manufacturer"] == "Bluelab"
        assert info["model"] == "IntelliLink"
        assert info["name"] == "Bluelab-AABE"
        assert ("bluelab", "gw-1") in info["identifiers"]


class TestGatewayDiagnosticSensorTypes:
    """Test gateway diagnostic sensor type definitions."""

    def test_gateway_sensor_types_count(self):
        """There are 6 gateway diagnostic sensor types."""
        from custom_components.bluelab.sensor import GATEWAY_SENSOR_TYPES

        assert len(GATEWAY_SENSOR_TYPES) == 6

    def test_gateway_sensor_types_keys(self):
        """Gateway sensor types cover all expected telemetry keys."""
        from custom_components.bluelab.sensor import GATEWAY_SENSOR_TYPES

        keys = {s["key"] for s in GATEWAY_SENSOR_TYPES}
        assert keys == {
            "current_fw_version",
            "fw_state",
            "eventsProduced",
            "eventsSent",
            "customconnectorEventsProduced",
            "customconnectorEventsSent",
        }

    def test_gateway_sensor_types_have_required_fields(self):
        """Each gateway sensor type has key, name, and entity_category diagnostic."""
        from custom_components.bluelab.sensor import GATEWAY_SENSOR_TYPES

        for sensor_type in GATEWAY_SENSOR_TYPES:
            assert "key" in sensor_type
            assert "name" in sensor_type
            assert sensor_type.get("entity_category") == "diagnostic"

    def test_event_sensors_have_total_increasing(self):
        """Event counter sensors have state_class total_increasing."""
        from custom_components.bluelab.sensor import GATEWAY_SENSOR_TYPES

        event_keys = {"eventsProduced", "eventsSent",
                      "customconnectorEventsProduced", "customconnectorEventsSent"}
        for sensor_type in GATEWAY_SENSOR_TYPES:
            if sensor_type["key"] in event_keys:
                assert sensor_type.get("state_class") == "total_increasing"

    def test_fw_sensors_have_no_state_class(self):
        """Firmware version and state sensors have no state_class."""
        from custom_components.bluelab.sensor import GATEWAY_SENSOR_TYPES

        fw_keys = {"current_fw_version", "fw_state"}
        for sensor_type in GATEWAY_SENSOR_TYPES:
            if sensor_type["key"] in fw_keys:
                assert sensor_type.get("state_class") is None

    def test_two_gateways_create_twelve_diagnostic_entities(self):
        """2 gateways × 6 sensors = 12 diagnostic entities."""
        from custom_components.bluelab.sensor import GATEWAY_SENSOR_TYPES

        gateways = [{"id": "gw-1"}, {"id": "gw-2"}]
        total = len(gateways) * len(GATEWAY_SENSOR_TYPES)
        assert total == 12


class TestTelemetryTimestamp:
    """Test telemetry timestamp exposed as entity attribute."""

    def test_last_reading_from_timestamp(self):
        """Telemetry sensor exposes last_reading as ISO 8601 UTC."""
        from custom_components.bluelab.sensor import format_telemetry_timestamp

        # 2025-12-28T16:48:32.515000+00:00
        result = format_telemetry_timestamp(1766940512515)
        assert result == "2025-12-28T16:48:32+00:00"

    def test_no_timestamp_returns_none(self):
        """No timestamp yields None."""
        from custom_components.bluelab.sensor import format_telemetry_timestamp

        assert format_telemetry_timestamp(None) is None
