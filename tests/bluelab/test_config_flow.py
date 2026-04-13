"""Tests for Bluelab IntelliDose config flow."""

import pytest
from aiohttp import ClientResponseError
from aioresponses import aioresponses
from unittest.mock import AsyncMock, patch

from custom_components.bluelab.const import (
    CONF_API_TOKEN,
    CONF_ORGANIZATION_ID,
    DEVICE_LIST_URL,
    DOMAIN,
)


MOCK_API_TOKEN = "test-api-token-123"
MOCK_ORG_ID = "org-456"
MOCK_DEVICES = [
    {"id": "dev-1", "name": "IDose1", "type": "intellidose"},
    {"id": "dev-2", "name": "IDose2", "type": "intellidose"},
]


@pytest.fixture
def mock_api():
    with aioresponses() as m:
        yield m


class TestConfigFlow:
    """Test the config flow."""

    @pytest.mark.asyncio
    async def test_valid_credentials(self, mock_api):
        """Config flow succeeds with valid API token and organization ID."""
        from custom_components.bluelab.config_flow import (
            validate_credentials,
        )

        mock_api.get(
            f"{DEVICE_LIST_URL}{MOCK_ORG_ID}",
            payload=MOCK_DEVICES,
            status=200,
        )

        devices = await validate_credentials(MOCK_API_TOKEN, MOCK_ORG_ID)
        assert len(devices) == 2
        assert devices[0]["name"] == "IDose1"

    @pytest.mark.asyncio
    async def test_invalid_api_token(self, mock_api):
        """Config flow rejects invalid API token with auth error."""
        from custom_components.bluelab.config_flow import (
            InvalidAuth,
            validate_credentials,
        )

        mock_api.get(
            f"{DEVICE_LIST_URL}{MOCK_ORG_ID}",
            status=401,
        )

        with pytest.raises(InvalidAuth):
            await validate_credentials("bad-token", MOCK_ORG_ID)

    @pytest.mark.asyncio
    async def test_invalid_organization_id(self, mock_api):
        """Config flow rejects invalid organization ID."""
        from custom_components.bluelab.config_flow import (
            InvalidOrganization,
            validate_credentials,
        )

        mock_api.get(
            f"{DEVICE_LIST_URL}bad-org",
            status=404,
        )

        with pytest.raises(InvalidOrganization):
            await validate_credentials(MOCK_API_TOKEN, "bad-org")
