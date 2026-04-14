## MODIFIED Requirements

### Requirement: Sensor entity creation per IntelliDose unit

The integration SHALL create HA sensor entities for each IntelliDose device returned by the device list API. Each non-gateway device SHALL have sensor entities for:

- EC (unit: "mS/cm", state_class: measurement)
- pH (unit: "pH", state_class: measurement)
- Temperature (device_class: temperature, unit: "°C", state_class: measurement)

Entity unique_id SHALL be derived from the Edenic device ID.

Each telemetry sensor entity SHALL expose an `extra_state_attributes` field named `last_reading` containing the telemetry timestamp as an ISO 8601 datetime string (UTC). If the timestamp is not available, `last_reading` SHALL be absent from attributes.

#### Scenario: Two IntelliDose devices and one gateway discovered

- **WHEN** the device list API returns two IntelliDose devices and one gateway
- **THEN** the integration SHALL create 10 telemetry/target sensor entities for the two IntelliDose devices, and 4 diagnostic sensor entities for the gateway (14 total)

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

### Requirement: Device registry organization

The integration SHALL register each device from the Edenic API as a HA device using the Edenic device ID as the identifier. For IntelliDose devices, the device entry SHALL use the `label` field as device name (falling back to `name` if `label` is null or empty), manufacturer "Bluelab", and model "IntelliDose". For gateway devices (`gateway: true`), the device entry SHALL use `additionalInfo.deviceIdentifier` as device name (falling back to `name`), manufacturer "Bluelab", and model "IntelliLink".

#### Scenario: IntelliDose appears with label

- **WHEN** the integration discovers an IntelliDose device with `label: "IDose"`
- **THEN** the HA device registry SHALL contain an entry with name "IDose", manufacturer "Bluelab", and model "IntelliDose"

#### Scenario: Gateway appears with deviceIdentifier

- **WHEN** the integration discovers a gateway device with `additionalInfo.deviceIdentifier: "Bluelab-7B69"`
- **THEN** the HA device registry SHALL contain an entry with name "Bluelab-7B69", manufacturer "Bluelab", and model "IntelliLink"

## ADDED Requirements

### Requirement: Gateway diagnostic entities

The integration SHALL create diagnostic sensor entities for each gateway device. The entities SHALL include:

- Firmware Version (value from `current_fw_version` telemetry key, entity_category: diagnostic)
- Firmware State (value from `fw_state` telemetry key, entity_category: diagnostic)
- Events Produced (value from `eventsProduced` telemetry key, state_class: total_increasing, entity_category: diagnostic)
- Events Sent (value from `eventsSent` telemetry key, state_class: total_increasing, entity_category: diagnostic)

#### Scenario: Gateway with diagnostic telemetry

- **WHEN** the gateway telemetry returns firmware version "0.0.1" and firmware state "UPDATED"
- **THEN** the integration SHALL create diagnostic sensor entities showing these values

#### Scenario: Gateway telemetry unavailable

- **WHEN** the gateway telemetry returns empty or errors
- **THEN** the gateway diagnostic entities SHALL be marked as unavailable
