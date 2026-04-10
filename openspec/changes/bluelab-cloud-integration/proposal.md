## Why

Three Bluelab IntelliDose controllers produce pH, EC, and temperature readings that need to surface in Home Assistant. The IntelliLink gateway sends this data to the Edenic cloud. BLE was explored and confirmed to carry only WiFi provisioning data, not sensor readings. The Edenic Cloud API (`api.edenic.io`) is the only available data source, with a documented REST API and an existing HA integration for Guardian WiFi (`maziggy/homeassistant-bluelab`) that proves the approach works for IntelliDose as well.

## What Changes

- Create a HA custom integration (`custom_components/bluelab/`) that polls the Edenic Cloud API for IntelliDose sensor data
- Authenticate via API token and organization ID (user-provided during config flow)
- Fetch telemetry (EC, pH, temperature) and device attributes (target setpoints) per device
- Create HA sensor entities per IntelliDose unit with proper device_class, unit_of_measurement, and state_class
- Respect the API rate limit of 1 request per minute (70-second polling interval)

## Non-Goals

- BLE connectivity — confirmed dead end for sensor data
- Local/offline data access — requires IntelliLink re-provisioning and traffic interception (future work)
- Writing to Edenic API (changing setpoints) — read-only integration
- Dashboard UI — handled by the separate `bluelab-dashboard-display` change
- Supporting Bluelab devices other than IntelliDose (Guardian, Pro Controller) — scope limited to IntelliDose

## Capabilities

### New Capabilities

- `bluelab-cloud-sensor`: HA integration that polls Edenic Cloud API for IntelliDose telemetry and exposes EC, pH, temperature, and target setpoints as HA sensor entities

### Modified Capabilities

(none)

## Impact

- New files: `custom_components/bluelab/` (manifest.json, __init__.py, sensor.py, config_flow.py, const.py, strings.json)
- Dependencies: `requests` (HTTP client, already available in HA)
- External dependency: Edenic Cloud API (`api.edenic.io`), requires user's API token + organization ID
- Reference implementation: `maziggy/homeassistant-bluelab` (Guardian WiFi integration using same API)
