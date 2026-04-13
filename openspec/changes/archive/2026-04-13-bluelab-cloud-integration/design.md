## Context

The Edenic Cloud API at `api.edenic.io` provides REST endpoints for reading Bluelab device telemetry and attributes. An existing HA integration (`maziggy/homeassistant-bluelab`) targets Guardian WiFi devices using this same API. Our integration targets IntelliDose controllers connected via IntelliLink. The API enforces a rate limit of 1 request per minute.

Relevant API endpoints (discovered from `maziggy/homeassistant-bluelab` source):
- `GET /api/v1/device/{org_id}` — list devices in an organization
- `GET /api/v1/telemetry/{device_id}` — latest sensor readings
- `GET /api/v1/device-attribute/{device_id}` — device attributes (target setpoints)

Authentication: `Authorization: {api_token}` header (no Bearer prefix based on reference implementation).

## Goals / Non-Goals

**Goals:**

- Read-only HA integration for IntelliDose telemetry via Edenic Cloud API
- Config flow with API token + organization ID validation
- Proper rate limiting to avoid API bans
- Entity naming and device grouping that matches the physical IntelliDose setup

**Non-Goals:**

- Write operations (changing setpoints via API)
- Supporting non-IntelliDose devices (Guardian, Pro Controller)
- Offline/local fallback — this integration requires cloud connectivity
- Replacing `maziggy/homeassistant-bluelab` — our integration is separate, focused on IntelliDose

## Decisions

### Build new integration rather than fork maziggy/homeassistant-bluelab

**Choice:** Write a new `custom_components/bluelab/` integration from scratch.

**Alternatives considered:**
- Fork `maziggy/homeassistant-bluelab`: it targets Guardian WiFi, mixes concerns (binary sensors, switches, number entities for Guardian-specific features), and uses synchronous `requests` in an async context. Adapting it for IntelliDose would require gutting most of the code.
- Contribute IntelliDose support to the existing repo: different device types have different telemetry shapes; merging them would complicate both.

**Rationale:** Cleaner to build focused IntelliDose support. We use the same API endpoints but with proper async HTTP (aiohttp/httpx), IntelliDose-specific entity mapping, and no Guardian baggage.

### Use aiohttp for API calls instead of requests

**Choice:** Use `aiohttp` (already bundled with HA) for all Edenic API calls.

**Alternatives considered:**
- `requests` via `async_add_executor_job`: works but wastes a thread pool slot per API call. The reference implementation does this and it's not ideal.

**Rationale:** HA best practice is native async. `aiohttp` is already a HA dependency, no additional requirements needed.

### Poll telemetry every 70 seconds with coordinator pattern

**Choice:** Use HA's `DataUpdateCoordinator` with a 70-second update interval for telemetry, and a separate coordinator for device attributes (also 70 seconds, offset by 35 seconds).

**Alternatives considered:**
- Single coordinator for both telemetry and attributes: would double the API calls per cycle if fetched together, risking rate limit.
- Longer interval (5 minutes): wastes the available API budget; 70 seconds is what Edenic allows.

**Rationale:** `DataUpdateCoordinator` handles error retry, logging, and entity update propagation. Staggering telemetry and attribute fetches avoids hitting the rate limit. With 3 IntelliDose devices, each telemetry cycle makes 3 requests spaced 5 seconds apart (as in the reference implementation).

## Risks / Trade-offs

- [Cloud dependency] If Edenic cloud is down or API changes, integration breaks. → Accept for now; future local interception work will provide a fallback.
- [Rate limiting with multiple devices] 3 devices × 1 req each = 3 requests per 70-second cycle, with 5-second delays between them. If Edenic's rate limit is per-request (not per-device), this could trigger throttling. → Start with 5-second inter-device delay; increase if 429 errors appear.
- [API token management] Token is stored in HA config entry (encrypted at rest by HA). No token refresh mechanism is known. → If token expires, user re-enters via config flow.
- [Unknown telemetry format for IntelliDose] The reference implementation targets Guardian. IntelliDose telemetry JSON shape might differ. → Implement defensively; log unknown fields; the user can verify against their Edenic dashboard once IntelliLink is re-provisioned.
