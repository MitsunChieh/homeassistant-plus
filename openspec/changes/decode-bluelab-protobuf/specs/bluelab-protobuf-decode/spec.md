## ADDED Requirements

### Requirement: Decode ABD binary payload into structured sensor data

The decoder SHALL accept a raw byte sequence from the Bluelab IntelliLink ABD BLE characteristic and return a list of per-device sensor readings. Each reading SHALL contain:

- Device name (string, e.g. "SC_AP", "Lini", "Line")
- EC value (float, mS/cm)
- pH value (float)
- Temperature value (float, °C)

The decoder SHALL return `None` for any sensor field that contains a null/no-reading marker (0xFFFFFFFF).

#### Scenario: Decode payload with three connected IntelliDose units

- **WHEN** the decoder receives an ABD payload containing data for three IntelliDose units with valid EC, pH, and temperature readings
- **THEN** it SHALL return three sensor reading objects, each with device name, EC, pH, and temperature values matching the physical display readings within ±0.1 tolerance

#### Scenario: Decode payload with missing sensor values

- **WHEN** the decoder receives an ABD payload where one or more sensor fields contain the null marker (0xFFFFFFFF bytes)
- **THEN** the corresponding field in the returned reading SHALL be `None`

#### Scenario: Decode payload with fewer than three devices

- **WHEN** the decoder receives an ABD payload containing data for fewer than three IntelliDose units
- **THEN** it SHALL return only the devices present in the payload, not pad to three

### Requirement: Decoder handles malformed input gracefully

The decoder SHALL raise a `DecodeError` exception when the input bytes do not conform to the expected binary structure.

#### Scenario: Empty payload

- **WHEN** the decoder receives an empty byte sequence
- **THEN** it SHALL raise `DecodeError`

#### Scenario: Truncated payload

- **WHEN** the decoder receives a byte sequence that is shorter than the minimum valid message length
- **THEN** it SHALL raise `DecodeError`

### Requirement: Validation dataset for regression testing

The project SHALL include a validation dataset containing at least two hex samples captured at different times, each paired with the corresponding physical display readings (EC, pH, temperature per unit). Tests SHALL verify the decoder output matches the expected readings.

#### Scenario: Decoder matches known readings at timestamp 13:42

- **WHEN** the decoder processes the hex sample captured at 13:42
- **THEN** the output SHALL match: IDose1 EC=1.2 pH=6.8 Temp=21, IDose2 EC=1.1 pH=6.7 Temp=20, IDose3 EC=1.9 pH=6.1 Temp=22

#### Scenario: Decoder matches known readings at timestamp 14:08

- **WHEN** the decoder processes the hex sample captured at 14:08
- **THEN** the output SHALL match: IDose1 EC=1.2 pH=7.0 Temp=21, IDose2 EC=1.1 pH=6.7 Temp=20, IDose3 EC=1.9 pH=6.1 Temp=22
