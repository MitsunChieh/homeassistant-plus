## 1. Validation Dataset

- [ ] 1.1 Create `tests/bluelab/test_data.py` with hex samples and expected readings for the validation dataset for regression testing — include 13:42 hex (from memory) and 14:08 hex (from LightBlue capture), each paired with display readings
- [ ] 1.2 Write failing tests in `tests/bluelab/test_decoder.py` that verify decoder matches known readings at timestamp 13:42 and timestamp 14:08 (TDD red phase)

## 2. Binary Format Analysis

- [ ] 2.1 Analyze ABD hex dumps to identify the protobuf/binary structure: field boundaries, encoding of device names (SC_AP, Lini, Line), numeric value encoding for EC/pH/temperature, and the null marker (0xFFFFFFFF) for missing sensor values

## 3. Core Decoder

- [ ] 3.1 Create `lib/bluelab/decoder.py` to decode ABD binary payload into structured sensor data — parse per-device fields, extract EC/pH/temperature floats, handle payload with fewer than three devices
- [ ] 3.2 Implement `DecodeError` exception so decoder handles malformed input gracefully — raise on empty payload, truncated payload, and structurally invalid input
- [ ] 3.3 Run test suite to verify all tests pass (TDD green phase)
