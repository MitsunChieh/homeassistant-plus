## Why

Edenic Cloud API telemetry includes a millisecond-epoch timestamp (`ts`) for each reading, but the current integration discards it during normalization. With the IntelliLink offline since 2025-12-28, all telemetry data is stale. Without exposing the timestamp, users have no way to know how old the displayed readings are.

## What Changes

- Preserve the telemetry timestamp during API response normalization
- Expose it as an `extra_state_attributes` field (`last_reading`) on each telemetry sensor entity, formatted as an ISO 8601 datetime string

## Non-Goals

- Changing polling intervals or coordinator behavior
- Adding timestamp to attribute (target setpoint) sensors — targets don't have per-reading timestamps

## Capabilities

### Modified Capabilities

- `bluelab-cloud-sensor`: Add telemetry timestamp as entity attribute

## Impact

- Modified files: `custom_components/bluelab/api.py`, `custom_components/bluelab/sensor.py`
- Modified tests: `tests/bluelab/test_api.py`, `tests/bluelab/test_sensor.py`
