"""Config flow for Bluelab IntelliDose integration."""

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_API_TOKEN,
    CONF_ORGANIZATION_ID,
    DEVICE_LIST_URL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_TOKEN): str,
        vol.Required(CONF_ORGANIZATION_ID): str,
    }
)


class InvalidAuth(Exception):
    """Error to indicate invalid authentication."""


class InvalidOrganization(Exception):
    """Error to indicate invalid organization ID."""


async def validate_credentials(
    api_token: str, organization_id: str
) -> list[dict[str, Any]]:
    """Validate credentials by fetching the device list.

    Returns the device list on success.
    Raises InvalidAuth for 401, InvalidOrganization for 404.
    """
    url = f"{DEVICE_LIST_URL}{organization_id}"
    headers = {"Authorization": api_token}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 401:
                raise InvalidAuth
            if response.status == 404:
                raise InvalidOrganization
            response.raise_for_status()
            return await response.json()


class BluelabConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bluelab IntelliDose."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                devices = await validate_credentials(
                    user_input[CONF_API_TOKEN],
                    user_input[CONF_ORGANIZATION_ID],
                )
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except InvalidOrganization:
                errors["base"] = "invalid_organization"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Bluelab ({len(devices)} devices)",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
