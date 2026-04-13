"""Constants for the Bluelab IntelliDose integration."""

from datetime import timedelta

DOMAIN = "bluelab"

# Edenic Cloud API
API_BASE_URL = "https://api.edenic.io/api/v1"
DEVICE_LIST_URL = f"{API_BASE_URL}/device/"
TELEMETRY_URL = f"{API_BASE_URL}/telemetry/"
DEVICE_ATTRIBUTE_URL = f"{API_BASE_URL}/device-attribute/"

# Config flow
CONF_API_TOKEN = "api_token"
CONF_ORGANIZATION_ID = "organization_id"

# Polling intervals
TELEMETRY_UPDATE_INTERVAL = timedelta(seconds=70)
ATTRIBUTE_UPDATE_INTERVAL = timedelta(seconds=70)
INTER_DEVICE_DELAY = 5  # seconds between requests for multiple devices
