## 1. Project Setup

- [x] 1.1 Initialize Next.js App Router project with TypeScript and Tailwind CSS for styling
- [x] 1.2 Configure environment variables (`HA_BASE_URL`, `HA_TOKEN`) in `.env.local` and `next.config.ts`
- [x] 1.3 Add `.env.local` to `.gitignore` and create `.env.example` with placeholder values

## 2. HA API Client (ha-api-client)

- [x] 2.1 Create HA API client abstraction `lib/ha-client.ts` with configurable HA connection: read `HA_BASE_URL` and `HA_TOKEN` from environment variables, implement `getStates()`, `getState(entityId)`, and `callService(domain, service, data)` functions
- [x] 2.2 Create server-side HA API proxy Route Handler `app/api/ha/states/route.ts` for fetching entity states (server-side HA API proxy requirement)
- [x] 2.3 Create server-side HA API proxy Route Handler `app/api/ha/services/route.ts` for forwarding service calls (token never exposed to browser)
- [x] 2.4 Implement polling-based state refresh on the client using SWR with configurable polling interval (default 5 seconds) — WebSocket via server-sent events (SSE) bridge deferred to future local server phase

## 3. Dashboard Layout and Grouping

- [x] 3.1 Create main dashboard page `app/page.tsx` with mobile-friendly layout (responsive from 320px viewport width)
- [x] 3.2 Implement area-based device grouping: fetch HA areas via API, group entities by area, place unassigned entities under "Other"
- [x] 3.3 Create reusable device card container component with area section headers (entity organization by HA areas)

## 4. Device Components (device-dashboard)

- [x] 4.1 Create light entity display and control component: show on/off state with visual indicator, brightness percentage, and toggle control that calls `services/light/toggle`
- [x] 4.2 Create temperature sensor display component: show current reading in °C, handle `unavailable`/`unknown` states with placeholder
- [x] 4.3 Create humidity sensor display component: show current reading as percentage
- [x] 4.4 Create climate entity display and control component: show current mode/target temp/current temp, controls for adjusting target temperature (`services/climate/set_temperature`) and changing AC mode (`services/climate/set_hvac_mode`)

## 5. HA Add-on Packaging

- [x] 5.1 Create Dockerfile for the Next.js dashboard add-on (multi-arch aarch64/amd64)
- [x] 5.2 Create HA add-on config files (`config.yaml`, `build.yaml`) with `HA_TOKEN` as add-on option
- [x] 5.3 Update `ha-client.ts` to use `http://homeassistant:8123` as default `HA_BASE_URL` (internal HA network)
- [ ] 5.4 Create add-on repository config (`repository.yaml`) for GitHub-based installation

## 6. Deployment

- [ ] 6.1 Add `dashboard.mitsun.cc` as Additional Host in Cloudflared add-on config, pointing to the dashboard add-on port
- [ ] 6.2 Build, install, and verify dashboard add-on loads with real HA data
