## Why

The Edenic API returns the IntelliLink gateway as a device alongside IntelliDose controllers. Currently the integration filters it out entirely. The gateway has useful diagnostic telemetry (firmware version, firmware state, event counters) that should be visible in HA. It also needs to be distinguished from IntelliDose devices — model should be "IntelliLink", not "IntelliDose".

## What Changes

- Remove the gateway filter — include IntelliLink gateway as a HA device
- Register gateway with model "IntelliLink" (not "IntelliDose") and use its `additionalInfo.deviceIdentifier` ("Bluelab-7B69") as device name
- Create diagnostic sensor entities for gateway: firmware version, firmware state, events produced, events sent
- Keep IntelliDose handling unchanged (EC/pH/temp/targets)

## Non-Goals

- WiFi RSSI from BLE — not available via Cloud API
- Gateway control or configuration
- Changing IntelliDose entity behavior

## Capabilities

### Modified Capabilities

- `bluelab-cloud-sensor`: Add IntelliLink gateway device with diagnostic entities, remove gateway filter

## Impact

- Modified files: `custom_components/bluelab/__init__.py`, `custom_components/bluelab/sensor.py`, `custom_components/bluelab/helpers.py`
- Modified tests: `tests/bluelab/test_device_filtering.py`, `tests/bluelab/test_sensor.py`
