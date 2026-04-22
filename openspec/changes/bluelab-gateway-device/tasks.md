## 1. Remove Gateway Filter

- [x] 1.1 Write failing test — verify gateway devices are no longer excluded from device list, and `filter_non_gateway_devices` is replaced with a function that classifies devices as gateway or IntelliDose (test with 2 gateways + 3 IntelliDose)
- [x] 1.2 Update `helpers.py` — replace `filter_non_gateway_devices` with `classify_devices` that returns separate gateway and IntelliDose lists; update `get_device_display_name` to handle gateway `additionalInfo.deviceIdentifier`
- [x] 1.3 Update `__init__.py` — pass both gateway and IntelliDose device lists for sensor entity creation per IntelliDose unit and gateway diagnostic entities; include all device IDs (gateways + IntelliDose) in telemetry polling with rate limit compliance
- [x] 1.4 Run tests to verify pass

## 2. Gateway Device Registration

- [x] 2.1 Write failing test for device registry organization — verify each gateway registered with model "IntelliLink" and name from `additionalInfo.deviceIdentifier`; verify IntelliDose still uses label and model "IntelliDose"
- [x] 2.2 Update `sensor.py` `make_device_info` to accept model parameter; create gateway devices with model "IntelliLink"
- [x] 2.3 Run tests to verify pass

## 3. Gateway Diagnostic Entities

- [ ] 3.1 Write failing test for gateway diagnostic entities — verify 6 diagnostic sensors per gateway (fw version, fw state, events produced, events sent, custom connector events produced, custom connector events sent) with correct entity_category; test with 2 gateways (12 diagnostic entities total)
- [ ] 3.2 Add `GATEWAY_SENSOR_TYPES` to `sensor.py` with 6 diagnostic sensor definitions (`current_fw_version`, `fw_state`, `eventsProduced`, `eventsSent`, `customconnectorEventsProduced`, `customconnectorEventsSent`); create `BluelabGatewayDiagnosticSensor` entity class; wire up in `async_setup_entry` for gateway devices
- [ ] 3.3 Run full test suite to verify all tests pass
