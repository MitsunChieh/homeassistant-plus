## Problem

The Bluelab integration creates sensor entities for all devices returned by the Edenic API, including the IntelliLink gateway. The gateway has no telemetry data, so its 5 entities all show "未知" (unknown). Additionally, device names display raw Edenic IDs (e.g. `42fb1c60-3c62-11f0-9521-8dff4b34f2dc__ASLID30301278`) instead of the human-readable `label` field from the API (e.g. "IDose").

## Root Cause

1. `__init__.py` passes all devices from the API to coordinators and sensor setup without filtering out `gateway: true` devices
2. `sensor.py` uses the `name` field (raw Edenic ID) instead of the `label` field for device display names

## Proposed Solution

1. Filter out devices where `gateway` is `true` before creating coordinators and entities
2. Use the `label` field as the device name, falling back to `name` only if `label` is null or empty

## Non-Goals

- Changing the gateway device model (it's not an IntelliDose)
- Adding gateway-specific entities (gateway has no useful telemetry)

## Success Criteria

- Gateway device does not appear in HA device registry
- IntelliDose devices show their label ("IDose", "IDose2") as device name
- Entity count: 2 devices × 5 entities = 10 (not 15)

## Impact

- Affected code: `custom_components/bluelab/__init__.py`, `custom_components/bluelab/sensor.py`
- Affected tests: `tests/bluelab/test_sensor.py`
