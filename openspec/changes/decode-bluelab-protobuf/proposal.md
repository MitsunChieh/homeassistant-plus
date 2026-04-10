## Why

Bluelab IntelliLink broadcasts sensor data (pH, EC, temperature) from connected IntelliDose controllers via BLE GATT characteristic ABD (Notify). The data arrives as binary payloads every ~5 seconds, likely protobuf-encoded. Without a decoder, this data is opaque and unusable. Decoding the format is the prerequisite for any HA integration or dashboard display.

## What Changes

- Reverse-engineer the ABD binary payload format using captured hex dumps cross-referenced with known sensor readings from three IntelliDose units
- Produce a Python decoder module that parses raw ABD bytes into structured sensor data (per-unit EC, pH, temperature, and their target setpoints)
- Include a validation dataset (hex samples + expected values) for regression testing

## Non-Goals

- BLE connectivity (connecting to IntelliLink, subscribing to notifications) — that belongs in a separate integration change
- HA entity creation or dashboard display
- Decoding ABF (config/auth) or ABE (command) characteristics — only ABD (sensor stream)
- Writing to IntelliLink (e.g., changing setpoints)

## Capabilities

### New Capabilities

- `bluelab-protobuf-decode`: Decode Bluelab IntelliLink ABD BLE characteristic binary payloads into structured sensor readings (EC, pH, temperature per IntelliDose unit)

### Modified Capabilities

(none)

## Impact

- New files: `lib/bluelab/decoder.py`, `tests/bluelab/test_decoder.py`
- No existing code affected — this is a standalone module
- Dependencies: Python 3.13; may add `protobuf` library if the format is standard protobuf, otherwise pure Python struct parsing
