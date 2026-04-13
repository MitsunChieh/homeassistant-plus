## 1. API Normalization

- [ ] 1.1 Write failing test for telemetry timestamp preservation — verify `_ts` key is present in normalized telemetry output
- [ ] 1.2 Update `_normalize_telemetry` in `api.py` to extract the most recent timestamp and include it as `_ts` (ms epoch) in the result dict
- [ ] 1.3 Run API tests to verify pass

## 2. Sensor Entity Attribute

- [ ] 2.1 Write failing test for telemetry timestamp exposed as attribute — verify `last_reading` in `extra_state_attributes` as ISO 8601 UTC; verify absent when no timestamp
- [ ] 2.2 Update sensor entity creation per IntelliDose unit — add `last_reading` to `BluelabTelemetrySensor` `extra_state_attributes` in `sensor.py` from coordinator data `_ts` field, converting ms epoch to ISO 8601 UTC
- [ ] 2.3 Run full test suite to verify all tests pass
