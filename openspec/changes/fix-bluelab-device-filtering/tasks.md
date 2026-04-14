## 1. Gateway Filtering

- [x] 1.1 Write failing test for gateway device excluded — verify devices with `gateway: true` are filtered out before entity creation
- [x] 1.2 Add gateway filtering in `__init__.py` — filter device list to exclude `gateway: true` before passing to coordinators and sensor setup; update sensor entity creation per IntelliDose unit
- [x] 1.3 Run tests to verify pass

## 2. Device Label as Name

- [x] 2.1 Write failing test for device registry organization — verify device name uses `label` field, falls back to `name` when label is null/empty
- [x] 2.2 Update `sensor.py` `make_device_info` and entity setup to use `label` field with fallback to `name` for device registry organization
- [x] 2.3 Run full test suite to verify all tests pass
