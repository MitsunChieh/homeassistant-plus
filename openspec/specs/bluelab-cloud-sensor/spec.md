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

The integration SHALL poll the Edenic Cloud API for telemetry data at a 70-second interval. For each device (both IntelliDose and gateway), it SHALL call `GET /api/v1/telemetry/{device_id}`. When multiple devices exist, requests SHALL be spaced at least 5 seconds apart to avoid triggering the API rate limit.

#### Scenario: Single device telemetry fetch

- **WHEN** the polling interval elapses and one device is configured
- **THEN** the integration SHALL fetch telemetry from `/api/v1/telemetry/{device_id}` and update sensor entity states

#### Scenario: Multiple device telemetry fetch with spacing

- **WHEN** the polling interval elapses and 5 devices are configured (2 gateways + 3 IntelliDose)
- **THEN** the integration SHALL fetch telemetry for each device with at least 5 seconds between requests

#### Scenario: API rate limit error

- **WHEN** the Edenic API returns HTTP 429 (rate limited)
- **THEN** the integration SHALL log a warning and retry at the next polling interval without marking entities as unavailable

---
### Requirement: Sensor entity creation per IntelliDose unit

The integration SHALL create HA sensor entities for each IntelliDose device returned by the device list API. Each non-gateway device (`gateway: false`) SHALL have sensor entities for:

- EC (unit: "mS/cm", state_class: measurement)
- pH (unit: "pH", state_class: measurement)
- Temperature (device_class: temperature, unit: "°C", state_class: measurement)

Entity unique_id SHALL be derived from the Edenic device ID.

Each telemetry sensor entity SHALL expose an `extra_state_attributes` field named `last_reading` containing the telemetry timestamp as an ISO 8601 datetime string (UTC). If the timestamp is not available, `last_reading` SHALL be absent from attributes.

Each gateway device (`gateway: true`) SHALL have 6 diagnostic sensor entities (see "Gateway diagnostic entities" requirement).

#### Scenario: Multiple IntelliDose devices and multiple gateways discovered

- **WHEN** the device list API returns 3 IntelliDose devices and 2 gateway devices
- **THEN** the integration SHALL create 15 telemetry/target sensor entities for the 3 IntelliDose devices (5 per device) and 12 diagnostic sensor entities for the 2 gateways (6 per gateway), totalling 27 entities

#### Scenario: Telemetry updates entity state

- **WHEN** new telemetry data is fetched for a device
- **THEN** the corresponding sensor entities SHALL update their state to reflect the latest EC, pH, and temperature values

#### Scenario: Device goes offline

- **WHEN** the telemetry API returns an error for a specific device (HTTP 400 or empty response)
- **THEN** the sensor entities for that device SHALL be marked as unavailable

#### Scenario: Telemetry timestamp exposed as attribute

- **WHEN** new telemetry data is fetched and contains a timestamp
- **THEN** each telemetry sensor entity SHALL have `last_reading` in its `extra_state_attributes` formatted as ISO 8601 UTC

#### Scenario: Telemetry without timestamp

- **WHEN** telemetry data does not contain a timestamp
- **THEN** the `last_reading` attribute SHALL NOT be present in `extra_state_attributes`

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

The integration SHALL register each device from the Edenic API as a HA device using the Edenic device ID as the identifier. For IntelliDose devices (`gateway: false`), the device entry SHALL use the `label` field as device name (falling back to `name` if `label` is null or empty), manufacturer "Bluelab", and model "IntelliDose". For gateway devices (`gateway: true`), the device entry SHALL use `additionalInfo.deviceIdentifier` as device name (falling back to `name`), manufacturer "Bluelab", and model "IntelliLink".

#### Scenario: IntelliDose appears with label

- **WHEN** the integration discovers an IntelliDose device with `label: "IDose A"`
- **THEN** the HA device registry SHALL contain an entry with name "IDose A", manufacturer "Bluelab", and model "IntelliDose"

#### Scenario: IntelliDose with no label falls back to name

- **WHEN** the integration discovers an IntelliDose device with `label: null`
- **THEN** the HA device registry SHALL use the `name` field as the device name

#### Scenario: Gateway appears with deviceIdentifier

- **WHEN** the integration discovers a gateway device with `additionalInfo.deviceIdentifier: "Bluelab-AABE"`
- **THEN** the HA device registry SHALL contain an entry with name "Bluelab-AABE", manufacturer "Bluelab", and model "IntelliLink"

---
### Requirement: Gateway diagnostic entities

The integration SHALL create diagnostic sensor entities for each gateway device (`gateway: true`). The entities SHALL include:

- Firmware Version (value from `current_fw_version` telemetry key, entity_category: diagnostic)
- Firmware State (value from `fw_state` telemetry key, entity_category: diagnostic)
- Events Produced (value from `eventsProduced` telemetry key, state_class: total_increasing, entity_category: diagnostic)
- Events Sent (value from `eventsSent` telemetry key, state_class: total_increasing, entity_category: diagnostic)
- Custom Connector Events Produced (value from `customconnectorEventsProduced` telemetry key, state_class: total_increasing, entity_category: diagnostic)
- Custom Connector Events Sent (value from `customconnectorEventsSent` telemetry key, state_class: total_increasing, entity_category: diagnostic)

#### Scenario: Gateway with diagnostic telemetry

- **WHEN** the gateway telemetry returns firmware version "0.0.1", firmware state "UPDATED", and event counters
- **THEN** the integration SHALL create 6 diagnostic sensor entities showing these values

#### Scenario: Gateway telemetry unavailable

- **WHEN** the gateway telemetry returns empty or errors
- **THEN** the gateway diagnostic entities SHALL be marked as unavailable

#### Scenario: Multiple gateways

- **WHEN** the device list API returns 2 gateway devices
- **THEN** the integration SHALL create 6 diagnostic sensor entities for each gateway (12 total), each with unique_id derived from the gateway's Edenic device ID
