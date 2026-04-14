## 1. Gateway Filtering

- [ ] 1.1 Write failing test for gateway device excluded — verify devices with `gateway: true` are filtered out before entity creation
- [ ] 1.2 Add gateway filtering in `__init__.py` — filter device list to exclude `gateway: true` before passing to coordinators and sensor setup; update sensor entity creation per IntelliDose unit
- [ ] 1.3 Run tests to verify pass

## 2. Device Label as Name

- [ ] 2.1 Write failing test for device registry organization — verify device name uses `label` field, falls back to `name` when label is null/empty
- [ ] 2.2 Update `sensor.py` `make_device_info` and entity setup to use `label` field with fallback to `name` for device registry organization
- [ ] 2.3 Run full test suite to verify all tests pass
