# device-dashboard Specification

## Purpose

TBD - created by archiving change 'build-ha-dashboard'. Update Purpose after archive.

## Requirements

### Requirement: Light entity display and control

The dashboard SHALL display all light entities with their current state (on/off) and brightness level. Users SHALL be able to toggle lights on/off.

#### Scenario: Light shown as on

- **WHEN** a light entity has state `on`
- **THEN** the dashboard SHALL display the light with a visual indicator showing it is on and its current brightness percentage

#### Scenario: Light shown as off

- **WHEN** a light entity has state `off`
- **THEN** the dashboard SHALL display the light with a visual indicator showing it is off

#### Scenario: Toggle light

- **WHEN** a user taps the toggle control on a light entity
- **THEN** the system SHALL call `services/light/toggle` for that entity and update the displayed state

---
### Requirement: Temperature sensor display

The dashboard SHALL display all temperature sensor entities with their current reading in degrees Celsius.

#### Scenario: Temperature reading displayed

- **WHEN** a temperature sensor entity has a numeric state value
- **THEN** the dashboard SHALL display the value with the unit `°C`

#### Scenario: Unavailable sensor

- **WHEN** a temperature sensor entity has state `unavailable` or `unknown`
- **THEN** the dashboard SHALL display a placeholder indicating the sensor is unavailable

---
### Requirement: Humidity sensor display

The dashboard SHALL display all humidity sensor entities with their current reading as a percentage.

#### Scenario: Humidity reading displayed

- **WHEN** a humidity sensor entity has a numeric state value
- **THEN** the dashboard SHALL display the value with the unit `%`

---
### Requirement: Climate entity display and control

The dashboard SHALL display climate entities (AC) with their current mode, target temperature, and current temperature. Users SHALL be able to adjust the target temperature and change the mode.

#### Scenario: AC status displayed

- **WHEN** a climate entity is active
- **THEN** the dashboard SHALL display the current mode (cool/heat/auto/off), target temperature, and current temperature

#### Scenario: Adjust target temperature

- **WHEN** a user adjusts the target temperature control on a climate entity
- **THEN** the system SHALL call `services/climate/set_temperature` with the new target value

#### Scenario: Change AC mode

- **WHEN** a user selects a different mode (cool/heat/auto/off) on a climate entity
- **THEN** the system SHALL call `services/climate/set_hvac_mode` with the selected mode

---
### Requirement: Area-based device grouping

The dashboard SHALL group entities by their assigned HA area (e.g., living room, bedroom). Entities without an area assignment SHALL appear under an "Other" group.

#### Scenario: Entities grouped by area

- **WHEN** the dashboard loads entity states
- **THEN** entities SHALL be visually grouped under their assigned area name

#### Scenario: Unassigned entities

- **WHEN** an entity has no area assignment in HA
- **THEN** the entity SHALL appear under a group labeled "Other"

---
### Requirement: Mobile-friendly layout

The dashboard SHALL render a responsive layout that is usable on mobile phone screens (viewport width 320px and above).

#### Scenario: Mobile viewport

- **WHEN** the dashboard is viewed on a screen with viewport width 320px
- **THEN** all device cards and controls SHALL be fully visible and operable without horizontal scrolling
