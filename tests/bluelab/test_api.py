"""Tests for Bluelab Edenic API client."""

import asyncio
import pytest
from aioresponses import aioresponses

from custom_components.bluelab.const import (
    DEVICE_LIST_URL,
    TELEMETRY_URL,
    DEVICE_ATTRIBUTE_URL,
)


MOCK_API_TOKEN = "test-api-token-123"
MOCK_ORG_ID = "org-456"
MOCK_DEVICES = [
    {"id": "dev-1", "name": "IDose1", "type": "intellidose"},
    {"id": "dev-2", "name": "IDose2", "type": "intellidose"},
    {"id": "dev-3", "name": "IDose3", "type": "intellidose"},
]
MOCK_TELEMETRY_RAW = {
    "ec": [{"ts": 1766940512515, "value": "1.98"}],
    "ph": [{"ts": 1766940512515, "value": "6.81"}],
    "nut_temp": [{"ts": 1766940512515, "value": "22.89"}],
}
MOCK_ATTRIBUTES_RAW = [
    {"lastUpdateTs": 1766940512515, "key": "setting.ec_set_point", "value": {"value": 2.2, "status": "SUCCESS"}},
    {"lastUpdateTs": 1766940512515, "key": "setting.ph_set_point", "value": {"value": 5.4, "status": "SUCCESS"}},
    {"lastUpdateTs": 1766940512515, "key": "some_other_attr", "value": "plain_string"},
]


@pytest.fixture
def mock_api():
    with aioresponses() as m:
        yield m


class TestEdenicApiClient:
    """Test the Edenic API client."""

    @pytest.mark.asyncio
    async def test_get_devices(self, mock_api):
        """Fetch device list from Edenic API."""
        from custom_components.bluelab.api import EdenicApiClient

        mock_api.get(
            f"{DEVICE_LIST_URL}{MOCK_ORG_ID}",
            payload=MOCK_DEVICES,
        )

        client = EdenicApiClient(MOCK_API_TOKEN)
        devices = await client.get_devices(MOCK_ORG_ID)
        assert len(devices) == 3
        assert devices[0]["id"] == "dev-1"

    @pytest.mark.asyncio
    async def test_get_telemetry(self, mock_api):
        """Fetch telemetry for a single device."""
        from custom_components.bluelab.api import EdenicApiClient

        mock_api.get(
            f"{TELEMETRY_URL}dev-1",
            payload=MOCK_TELEMETRY_RAW,
        )

        client = EdenicApiClient(MOCK_API_TOKEN)
        data = await client.get_telemetry("dev-1")
        assert data["ec"] == 1.98
        assert data["ph"] == 6.81
        assert data["nut_temp"] == 22.89

    @pytest.mark.asyncio
    async def test_get_device_attributes(self, mock_api):
        """Fetch device attributes (target setpoints)."""
        from custom_components.bluelab.api import EdenicApiClient

        mock_api.get(
            f"{DEVICE_ATTRIBUTE_URL}dev-1",
            payload=MOCK_ATTRIBUTES_RAW,
        )

        client = EdenicApiClient(MOCK_API_TOKEN)
        data = await client.get_device_attributes("dev-1")
        assert data["setting.ec_set_point"] == 2.2
        assert data["setting.ph_set_point"] == 5.4

    @pytest.mark.asyncio
    async def test_get_telemetry_multiple_devices_with_spacing(self, mock_api):
        """Fetch telemetry for multiple devices respects inter-device delay."""
        from custom_components.bluelab.api import EdenicApiClient

        for dev in MOCK_DEVICES:
            mock_api.get(
                f"{TELEMETRY_URL}{dev['id']}",
                payload=MOCK_TELEMETRY_RAW,
            )

        client = EdenicApiClient(MOCK_API_TOKEN)

        start = asyncio.get_event_loop().time()
        results = await client.get_telemetry_all_devices(
            [d["id"] for d in MOCK_DEVICES], inter_device_delay=0.1
        )
        elapsed = asyncio.get_event_loop().time() - start

        assert len(results) == 3
        # 3 devices with 0.1s delay between = at least 0.2s total
        assert elapsed >= 0.2

    @pytest.mark.asyncio
    async def test_rate_limit_error_raises(self, mock_api):
        """HTTP 429 raises RateLimitError."""
        from custom_components.bluelab.api import EdenicApiClient, RateLimitError

        mock_api.get(
            f"{TELEMETRY_URL}dev-1",
            status=429,
        )

        client = EdenicApiClient(MOCK_API_TOKEN)
        with pytest.raises(RateLimitError):
            await client.get_telemetry("dev-1")

    @pytest.mark.asyncio
    async def test_auth_error_raises(self, mock_api):
        """HTTP 401 raises AuthError."""
        from custom_components.bluelab.api import EdenicApiClient, AuthError

        mock_api.get(
            f"{TELEMETRY_URL}dev-1",
            status=401,
        )

        client = EdenicApiClient(MOCK_API_TOKEN)
        with pytest.raises(AuthError):
            await client.get_telemetry("dev-1")
