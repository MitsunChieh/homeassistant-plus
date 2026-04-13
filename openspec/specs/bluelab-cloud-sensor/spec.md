# bluelab-cloud-sensor Specification

## Purpose

TBD - created by archiving change 'bluelab-cloud-integration'. Update Purpose after archive.

## Requirements

### Requirement: Config flow with API token and organization ID

The integration SHALL provide a config flow that accepts an Edenic API token and organization ID. The config flow SHALL validate the credentials by calling `GET /api/v1/device/{org_id}` and SHALL reject invalid credentials with a descriptive error message.

#### Scenario: Valid credentials

- **WHEN** the user enters a valid API token and organization ID in the config flow
- **THEN** the integration SHALL successfully connect to the Edenic API, fetch the device list, and complete setup

#### Scenario: Invalid API token

- **WHEN** the user enters an invalid API token
- **THEN** the integration SHALL display an authentication error and NOT complete setup

#### Scenario: Invalid organization ID

- **WHEN** the user enters a valid API token but an invalid organization ID
- **THEN** the integration SHALL display an error indicating the organization was not found

---
### Requirement: Telemetry polling with rate limit compliance

The integration SHALL poll the Edenic Cloud API for telemetry data at a 70-second interval. For each IntelliDose device, it SHALL call `GET /api/v1/telemetry/{device_id}`. When multiple devices exist, requests SHALL be spaced at least 5 seconds apart to avoid triggering the API rate limit.

#### Scenario: Single device telemetry fetch

- **WHEN** the polling interval elapses and one IntelliDose device is configured
- **THEN** the integration SHALL fetch telemetry from `/api/v1/telemetry/{device_id}` and update sensor entity states

#### Scenario: Multiple device telemetry fetch with spacing

- **WHEN** the polling interval elapses and three IntelliDose devices are configured
- **THEN** the integration SHALL fetch telemetry for each device with at least 5 seconds between requests

#### Scenario: API rate limit error

- **WHEN** the Edenic API returns HTTP 429 (rate limited)
- **THEN** the integration SHALL log a warning and retry at the next polling interval without marking entities as unavailable

---
### Requirement: Sensor entity creation per IntelliDose unit

The integration SHALL create HA sensor entities for each IntelliDose device returned by the device list API. Each device SHALL have sensor entities for:

- EC (unit: "mS/cm", state_class: measurement)
- pH (unit: "pH", state_class: measurement)
- Temperature (device_class: temperature, unit: "°C", state_class: measurement)

Entity unique_id SHALL be derived from the Edenic device ID.

#### Scenario: Three IntelliDose devices discovered

- **WHEN** the device list API returns three IntelliDose devices
- **THEN** the integration SHALL create 9 sensor entities (3 devices × 3 sensors) with appropriate unit_of_measurement and state_class

#### Scenario: Telemetry updates entity state

- **WHEN** new telemetry data is fetched for a device
- **THEN** the corresponding sensor entities SHALL update their state to reflect the latest EC, pH, and temperature values

#### Scenario: Device goes offline

- **WHEN** the telemetry API returns an error for a specific device (HTTP 400 or empty response)
- **THEN** the sensor entities for that device SHALL be marked as unavailable

---
### Requirement: Target setpoint entities from device attributes

The integration SHALL fetch device attributes from `GET /api/v1/device-attribute/{device_id}` and create additional sensor entities for EC target and pH target setpoints per device.

#### Scenario: Target setpoints displayed

- **WHEN** the device attributes API returns target values for EC and pH
- **THEN** the integration SHALL create sensor entities showing the current target setpoints (EC target in mS/cm, pH target in pH)

#### Scenario: Attributes update interval

- **WHEN** 70 seconds have elapsed since the last attribute fetch
- **THEN** the integration SHALL fetch updated device attributes, offset from telemetry fetches to distribute API load

---
### Requirement: Device registry organization

The integration SHALL register each IntelliDose as a HA device using the Edenic device ID as the identifier. The device entry SHALL include the device name from the Edenic API, manufacturer "Bluelab", and model "IntelliDose".

#### Scenario: Device appears in HA device registry

- **WHEN** the integration discovers an IntelliDose device from the API
- **THEN** the HA device registry SHALL contain an entry with manufacturer "Bluelab", model "IntelliDose", and the device name from the Edenic API
