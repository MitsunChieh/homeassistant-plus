## MODIFIED Requirements

### Requirement: Sensor entity creation per IntelliDose unit

The integration SHALL create HA sensor entities for each IntelliDose device returned by the device list API. Devices where `gateway` is `true` SHALL be excluded — no entities SHALL be created for gateway devices. Each non-gateway device SHALL have sensor entities for:

- EC (unit: "mS/cm", state_class: measurement)
- pH (unit: "pH", state_class: measurement)
- Temperature (device_class: temperature, unit: "°C", state_class: measurement)

Entity unique_id SHALL be derived from the Edenic device ID.

Each telemetry sensor entity SHALL expose an `extra_state_attributes` field named `last_reading` containing the telemetry timestamp as an ISO 8601 datetime string (UTC). If the timestamp is not available, `last_reading` SHALL be absent from attributes.

#### Scenario: Gateway device excluded

- **WHEN** the device list API returns a device with `gateway: true`
- **THEN** the integration SHALL NOT create any entities for that device and it SHALL NOT appear in the HA device registry

#### Scenario: Two IntelliDose devices discovered

- **WHEN** the device list API returns two IntelliDose devices and one gateway
- **THEN** the integration SHALL create 10 sensor entities (2 devices × 5 sensors each) and exclude the gateway

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

The integration SHALL register each IntelliDose as a HA device using the Edenic device ID as the identifier. The device entry SHALL include the device label from the Edenic API as the device name (falling back to the raw `name` field if `label` is null or empty), manufacturer "Bluelab", and model "IntelliDose".

#### Scenario: Device appears in HA device registry with label

- **WHEN** the integration discovers an IntelliDose device with `label: "IDose"`
- **THEN** the HA device registry SHALL contain an entry with name "IDose", manufacturer "Bluelab", and model "IntelliDose"

#### Scenario: Device with no label falls back to name

- **WHEN** the integration discovers an IntelliDose device with `label: null`
- **THEN** the HA device registry SHALL use the `name` field as the device name
