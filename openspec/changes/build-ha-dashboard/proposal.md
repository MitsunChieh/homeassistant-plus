## Why

Home Assistant's native UI exposes settings, automations, and developer tools that overwhelm non-technical household members. A simplified, read-and-control dashboard lets family members check device states and perform basic operations (lights, temperature, AC) without risk of misconfiguring the system.

## What Changes

- Create a Next.js (App Router) web application with a clean, mobile-friendly dashboard UI
- Connect to HA REST API via localhost (running as an HA add-on on the same device) using a Long-Lived Access Token
- Display real-time device states: lights (on/off/brightness), temperature sensors, humidity sensors, and climate entities (AC)
- Provide simple controls: toggle lights, adjust AC temperature/mode
- Package as a custom HA add-on (Docker container), hosted in a GitHub repository for easy installation
- Expose externally via Cloudflare Tunnel Additional Hosts (`dashboard.mitsun.cc`)

## Capabilities

### New Capabilities

- `ha-api-client`: Home Assistant API client that handles REST connections and authentication via Long-Lived Access Token, running server-side as an HA add-on
- `device-dashboard`: Web dashboard UI showing device states (lights, temperature, humidity, AC) with simple toggle and adjustment controls, organized by room or area

### Modified Capabilities

(none)

## Impact

- New codebase: Next.js project with App Router, Tailwind CSS
- External dependencies: Home Assistant REST API
- Deployment: HA add-on (Docker container on Odroid N2), GitHub repo for distribution
- External access: Cloudflare Tunnel Additional Hosts (`dashboard.mitsun.cc`)
- Add-on configuration: `HA_TOKEN` provided via add-on config UI, `HA_BASE_URL` defaults to `http://homeassistant:8123`
- Consumes existing spec: `remote-access` (Cloudflare Tunnel + Access)
