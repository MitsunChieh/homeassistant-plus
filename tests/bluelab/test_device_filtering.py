"""Tests for device classification and label naming."""

import pytest


MOCK_DEVICES = [
    {"id": "gw-1", "name": "org__b827eb978496", "label": None, "gateway": True,
     "additionalInfo": {"gateway": True, "deviceIdentifier": "Bluelab-7B69"}},
    {"id": "gw-2", "name": "org__b827ebaf5541", "label": None, "gateway": True,
     "additionalInfo": {"gateway": True, "deviceIdentifier": "Bluelab-AABE"}},
    {"id": "dev-1", "name": "org__ASLID30301278", "label": "IDose A", "gateway": False,
     "additionalInfo": {"lastConnectedGateway": "gw-1"}},
    {"id": "dev-2", "name": "org__ASLID50501061", "label": "IDose B", "gateway": False,
     "additionalInfo": {"lastConnectedGateway": "gw-2"}},
    {"id": "dev-3", "name": "org__ASLID50501036", "label": "IDose C", "gateway": False,
     "additionalInfo": {"lastConnectedGateway": "gw-2"}},
]


class TestClassifyDevices:
    """Test that devices are classified into gateways and IntelliDose."""

    def test_classify_separates_gateways_and_intellidose(self):
        """classify_devices returns separate gateway and IntelliDose lists."""
        from custom_components.bluelab.helpers import classify_devices

        gateways, intellidose = classify_devices(MOCK_DEVICES)
        assert len(gateways) == 2
        assert len(intellidose) == 3

    def test_classify_gateways_have_gateway_true(self):
        """All devices in the gateways list have gateway=True."""
        from custom_components.bluelab.helpers import classify_devices

        gateways, _ = classify_devices(MOCK_DEVICES)
        assert all(d["gateway"] for d in gateways)

    def test_classify_intellidose_have_gateway_false(self):
        """All devices in the IntelliDose list have gateway=False."""
        from custom_components.bluelab.helpers import classify_devices

        _, intellidose = classify_devices(MOCK_DEVICES)
        assert all(not d["gateway"] for d in intellidose)

    def test_classify_preserves_device_ids(self):
        """All original device IDs are present across both lists."""
        from custom_components.bluelab.helpers import classify_devices

        gateways, intellidose = classify_devices(MOCK_DEVICES)
        gw_ids = {d["id"] for d in gateways}
        dose_ids = {d["id"] for d in intellidose}
        assert gw_ids == {"gw-1", "gw-2"}
        assert dose_ids == {"dev-1", "dev-2", "dev-3"}

    def test_classify_empty_list(self):
        """Empty input returns two empty lists."""
        from custom_components.bluelab.helpers import classify_devices

        gateways, intellidose = classify_devices([])
        assert gateways == []
        assert intellidose == []


class TestDeviceLabel:
    """Test that device name uses label with fallback."""

    def test_label_used_as_name(self):
        """IntelliDose with label uses label as name."""
        from custom_components.bluelab.helpers import get_device_display_name

        assert get_device_display_name(MOCK_DEVICES[2]) == "IDose A"

    def test_label_null_falls_back_to_name(self):
        """Device with null label falls back to name field."""
        from custom_components.bluelab.helpers import get_device_display_name

        device = {"id": "x", "name": "org__fallback", "label": None, "gateway": False}
        assert get_device_display_name(device) == "org__fallback"

    def test_label_empty_falls_back_to_name(self):
        """Device with empty string label falls back to name."""
        from custom_components.bluelab.helpers import get_device_display_name

        device = {"id": "x", "name": "fallback", "label": "   ", "gateway": False}
        assert get_device_display_name(device) == "fallback"

    def test_gateway_uses_device_identifier(self):
        """Gateway uses additionalInfo.deviceIdentifier as display name."""
        from custom_components.bluelab.helpers import get_device_display_name

        assert get_device_display_name(MOCK_DEVICES[0]) == "Bluelab-7B69"
        assert get_device_display_name(MOCK_DEVICES[1]) == "Bluelab-AABE"

    def test_gateway_without_device_identifier_falls_back(self):
        """Gateway without deviceIdentifier falls back to name."""
        from custom_components.bluelab.helpers import get_device_display_name

        device = {"id": "gw-x", "name": "org__fallback", "label": None, "gateway": True,
                  "additionalInfo": {"gateway": True}}
        assert get_device_display_name(device) == "org__fallback"
