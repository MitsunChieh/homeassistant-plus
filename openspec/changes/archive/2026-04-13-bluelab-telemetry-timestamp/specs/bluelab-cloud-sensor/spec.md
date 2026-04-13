## MODIFIED Requirements

### Requirement: Sensor entity creation per IntelliDose unit

The integration SHALL create HA sensor entities for each IntelliDose device returned by the device list API. Each device SHALL have sensor entities for:

- EC (unit: "mS/cm", state_class: measurement)
- pH (unit: "pH", state_class: measurement)
- Temperature (device_class: temperature, unit: "°C", state_class: measurement)

Entity unique_id SHALL be derived from the Edenic device ID.

Each telemetry sensor entity SHALL expose an `extra_state_attributes` field named `last_reading` containing the telemetry timestamp as an ISO 8601 datetime string (UTC). If the timestamp is not available, `last_reading` SHALL be absent from attributes.

#### Scenario: Three IntelliDose devices discovered

- **WHEN** the device list API returns three IntelliDose devices
- **THEN** the integration SHALL create 9 sensor entities (3 devices × 3 sensors) with appropriate unit_of_measurement and state_class

#### Scenario: Telemetry updates entity state

- **WHEN** new telemetry data is fetched for a device
- **THEN** the corresponding sensor entities SHALL update their state to reflect the latest EC, pH, and temperature values

#### Scenario: Device goes offline

- **WHEN** the telemetry API returns an error for a specific device (HTTP 400 or empty response)
- **THEN** the sensor entities for that device SHALL be marked as unavailable

#### Scenario: Telemetry timestamp exposed as attribute

- **WHEN** new telemetry data is fetched and contains a timestamp
- **THEN** each telemetry sensor entity SHALL have `last_reading` in its `extra_state_attributes` formatted as ISO 8601 UTC (e.g. "2025-12-28T16:48:32+00:00")

#### Scenario: Telemetry without timestamp

- **WHEN** telemetry data does not contain a timestamp
- **THEN** the `last_reading` attribute SHALL NOT be present in `extra_state_attributes`
