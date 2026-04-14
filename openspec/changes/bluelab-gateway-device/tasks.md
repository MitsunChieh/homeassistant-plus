## 1. Remove Gateway Filter

- [ ] 1.1 Write failing test — verify gateway device is no longer excluded from device list, and `filter_non_gateway_devices` is replaced with a function that classifies devices as gateway or intellidose
- [ ] 1.2 Update `helpers.py` — replace `filter_non_gateway_devices` with `classify_devices` that returns separate gateway and intellidose lists; update `get_device_display_name` to handle gateway `additionalInfo.deviceIdentifier`
- [ ] 1.3 Update `__init__.py` — pass both gateway and intellidose device lists for sensor entity creation per IntelliDose unit and gateway diagnostic entities; include all device IDs in telemetry coordinator
- [ ] 1.4 Run tests to verify pass

## 2. Gateway Device Registration

- [ ] 2.1 Write failing test for device registry organization — verify gateway registered with model "IntelliLink" and name from `additionalInfo.deviceIdentifier`
- [ ] 2.2 Update `sensor.py` `make_device_info` to accept model parameter; create gateway devices with model "IntelliLink"
- [ ] 2.3 Run tests to verify pass

## 3. Gateway Diagnostic Entities

- [ ] 3.1 Write failing test for gateway diagnostic entities — verify 4 diagnostic sensors (fw version, fw state, events produced, events sent) with correct entity_category
- [ ] 3.2 Add `GATEWAY_SENSOR_TYPES` to `sensor.py` with the 4 diagnostic sensor definitions; create `BluelabGatewayDiagnosticSensor` entity class; wire up in `async_setup_entry` for gateway devices
- [ ] 3.3 Run full test suite to verify all tests pass
