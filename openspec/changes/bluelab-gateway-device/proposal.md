## Why

The Edenic API returns IntelliLink gateways as devices alongside IntelliDose controllers. Currently the integration filters them out entirely. Gateways have useful diagnostic telemetry (firmware version, firmware state, event counters) that should be visible in HA. They also need to be distinguished from IntelliDose devices — model should be "IntelliLink", not "IntelliDose".

As of 2026-04-22, the API returns 2 gateways (Bluelab-7B69, Bluelab-AABE) and 3 IntelliDose (IDose A, IDose B, IDose C). The integration must handle multiple gateways.

## What Changes

- Remove the gateway filter — include IntelliLink gateways as HA devices
- Register each gateway with model "IntelliLink" (not "IntelliDose") and use its `additionalInfo.deviceIdentifier` (e.g. "Bluelab-AABE") as device name
- Create 6 diagnostic sensor entities per gateway: firmware version, firmware state, events produced, events sent, custom connector events produced, custom connector events sent
- Keep IntelliDose handling unchanged (EC/pH/temp/targets)

## Non-Goals

- WiFi RSSI from BLE — not available via Cloud API
- Gateway control or configuration
- Changing IntelliDose entity behavior

## Capabilities

### Modified Capabilities

- `bluelab-cloud-sensor`: Add IntelliLink gateway devices with diagnostic entities, remove gateway filter

## Impact

- Modified files: `custom_components/bluelab/__init__.py`, `custom_components/bluelab/sensor.py`, `custom_components/bluelab/helpers.py`
- Modified tests: `tests/bluelab/test_device_filtering.py`, `tests/bluelab/test_sensor.py`
