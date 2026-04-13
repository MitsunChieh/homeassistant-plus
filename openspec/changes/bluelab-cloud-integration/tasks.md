## 1. Integration Scaffold

- [x] 1.1 Create `custom_components/bluelab/` with `manifest.json` (domain: bluelab, dependencies: [], requirements: []), `const.py` (API URLs, polling intervals, domain constant), and `__init__.py` stub — build new integration rather than fork maziggy/homeassistant-bluelab
- [x] 1.2 Write failing tests for config flow with API token and organization ID — test valid credentials, invalid API token, and invalid organization ID scenarios

## 2. Config Flow

- [x] 2.1 Implement config flow with API token and organization ID in `config_flow.py` — validate credentials by calling `GET /api/v1/device/{org_id}`, reject invalid credentials with descriptive error messages
- [x] 2.2 Create `strings.json` and `translations/en.json` with config flow UI strings (step titles, field labels, error messages)
- [x] 2.3 Run tests to verify config flow tests pass

## 3. API Client and Coordinators

- [x] 3.1 Write failing tests for telemetry polling with rate limit compliance — test single device fetch, multiple device fetch with spacing, and API rate limit error handling
- [x] 3.2 Implement Edenic API client in `api.py` — use aiohttp for API calls instead of requests; methods for device list, telemetry, and device attributes; handle auth header and HTTP errors
- [x] 3.3 Implement telemetry `DataUpdateCoordinator` in `coordinator.py` — poll telemetry every 70 seconds with coordinator pattern, space multiple device requests 5 seconds apart
- [x] 3.4 Implement attribute `DataUpdateCoordinator` in `coordinator.py` — fetch device attributes at 70-second interval offset from telemetry, for target setpoint entities from device attributes
- [x] 3.5 Run tests to verify API client and coordinator tests pass

## 4. Sensor Entities

- [ ] 4.1 Write failing tests for sensor entity creation per IntelliDose unit — test 3 devices × 3 sensors, telemetry state updates, device offline handling, and target setpoint entities
- [ ] 4.2 Implement `sensor.py` — create EC, pH, temperature entities per device with proper unit_of_measurement and state_class; create EC target and pH target entities from device attributes; handle unavailable state
- [ ] 4.3 Implement device registry organization — register each IntelliDose with manufacturer "Bluelab", model "IntelliDose", and Edenic device name
- [ ] 4.4 Wire up coordinators in `__init__.py` `async_setup_entry` — create coordinators, trigger initial fetch, forward to sensor platform
- [ ] 4.5 Run full test suite to verify all tests pass
