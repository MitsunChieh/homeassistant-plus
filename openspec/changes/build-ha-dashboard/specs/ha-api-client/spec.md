## ADDED Requirements

### Requirement: Server-side HA API proxy

The system SHALL proxy all Home Assistant API requests through Next.js server-side Route Handlers. The HA base URL and Long-Lived Access Token MUST NOT be exposed to the browser client.

#### Scenario: Client requests entity states

- **WHEN** the browser client requests device states
- **THEN** the server-side Route Handler SHALL fetch states from `{HA_BASE_URL}/api/states` using the `HA_TOKEN` and return the result to the client

#### Scenario: Client sends a service call

- **WHEN** the browser client sends a control command (e.g., toggle light)
- **THEN** the server-side Route Handler SHALL forward the request to `{HA_BASE_URL}/api/services/{domain}/{service}` using the `HA_TOKEN`

#### Scenario: Token never exposed

- **WHEN** any page or API response is inspected in the browser
- **THEN** the `HA_TOKEN` and `HA_BASE_URL` values MUST NOT appear in HTML source, JavaScript bundles, or network response headers

### Requirement: Configurable HA connection

The HA API client SHALL read `HA_BASE_URL` and `HA_TOKEN` from environment variables. Changing the base URL MUST NOT require code changes.

#### Scenario: Switch from Cloudflare Tunnel to local server

- **WHEN** the `HA_BASE_URL` environment variable is changed from `https://homeassistant.mitsun.cc` to a local server address
- **THEN** all API calls SHALL use the new base URL without any code modifications

### Requirement: Polling-based state refresh

The system SHALL poll the HA REST API at a configurable interval (default 5 seconds) to retrieve current entity states.

#### Scenario: Automatic state refresh

- **WHEN** the dashboard is open in a browser
- **THEN** the system SHALL fetch updated entity states from HA every 5 seconds

#### Scenario: Custom polling interval

- **WHEN** the polling interval is configured to a value other than 5 seconds
- **THEN** the system SHALL use the configured interval for state refresh
