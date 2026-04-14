"""Tests for device filtering and label naming."""

import pytest


MOCK_DEVICES = [
    {"id": "gw-1", "name": "org__b827eb978496", "label": None, "gateway": True},
    {"id": "dev-1", "name": "org__ASLID30301278", "label": "IDose     ", "gateway": False},
    {"id": "dev-2", "name": "org__ASLID50501061", "label": "IDose2", "gateway": False},
]


class TestGatewayFiltering:
    """Test that gateway devices are excluded."""

    def test_filter_excludes_gateway(self):
        """Devices with gateway=True are filtered out."""
        from custom_components.bluelab.helpers import filter_non_gateway_devices

        result = filter_non_gateway_devices(MOCK_DEVICES)
        assert len(result) == 2
        assert all(not d["gateway"] for d in result)

    def test_filter_keeps_intellidose(self):
        """Non-gateway devices are kept."""
        from custom_components.bluelab.helpers import filter_non_gateway_devices

        result = filter_non_gateway_devices(MOCK_DEVICES)
        ids = [d["id"] for d in result]
        assert "dev-1" in ids
        assert "dev-2" in ids
        assert "gw-1" not in ids


class TestDeviceLabel:
    """Test that device name uses label with fallback."""

    def test_label_used_as_name(self):
        """Device with label uses label (stripped) as name."""
        from custom_components.bluelab.helpers import get_device_display_name

        assert get_device_display_name(MOCK_DEVICES[1]) == "IDose"

    def test_label_null_falls_back_to_name(self):
        """Device with null label falls back to name field."""
        from custom_components.bluelab.helpers import get_device_display_name

        assert get_device_display_name(MOCK_DEVICES[0]) == "org__b827eb978496"

    def test_label_empty_falls_back_to_name(self):
        """Device with empty string label falls back to name."""
        from custom_components.bluelab.helpers import get_device_display_name

        device = {"id": "x", "name": "fallback", "label": "   ", "gateway": False}
        assert get_device_display_name(device) == "fallback"
