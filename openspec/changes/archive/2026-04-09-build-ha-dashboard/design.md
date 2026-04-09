## Context

Home Assistant runs on an Odroid N2 behind a Cloudflare Tunnel (`homeassistant.mitsun.cc`) with Cloudflare Access (email OTP) protecting the endpoint. The dashboard needs to call HA's API through this tunnel from a Vercel-deployed Next.js app. The HA API token must never be exposed to the browser.

## Goals / Non-Goals

**Goals:**

- Simple, mobile-friendly dashboard for non-technical users
- Real-time state updates for lights, temperature, humidity, and AC
- Server-side API calls to keep the HA token secure
- Configurable base URL to support future infrastructure changes

**Non-Goals:**

- Replacing HA's UI for admin users — this dashboard is view-and-control only
- Supporting HA add-on installation, automation editing, or integration management
- User authentication system — Cloudflare Access handles this layer
- Offline/PWA support
- Historical data charts or energy monitoring

## Decisions

### Next.js App Router with server-side API proxy

Use Next.js App Router with Route Handlers (`app/api/`) to proxy all HA API calls server-side. The browser never sees the HA token or base URL.

**Why not client-side API calls**: The Long-Lived Access Token would be exposed in browser network requests. Even with Cloudflare Access, leaking the token is unacceptable — it grants full HA control.

**Why not a separate backend**: Next.js Route Handlers serve the same purpose with zero additional infrastructure.

### WebSocket via server-sent events (SSE) bridge

HA's WebSocket API provides real-time state updates. Since Vercel serverless functions cannot maintain persistent WebSocket connections, use a polling-based approach with SWR/React Query for automatic revalidation on the client, with server-side Route Handlers fetching current state from HA REST API.

**Why not direct WebSocket from browser**: Would expose the HA token client-side.

**Why not SSE from server**: Vercel serverless functions have execution time limits (10-60s on free tier), making persistent connections impractical.

**Future option**: When migrating to a local server, a true WebSocket proxy can replace polling for instant updates.

### Tailwind CSS for styling

Tailwind provides utility-first styling with no component library lock-in. The dashboard UI is simple enough (cards, toggles, sliders) that a component library like shadcn/ui or MUI adds unnecessary weight.

### HA API client abstraction

Create a single `lib/ha-client.ts` module that encapsulates all HA API communication. The base URL and token are read from environment variables (`HA_BASE_URL`, `HA_TOKEN`). All Route Handlers import from this module.

**Why abstract**: Switching from Cloudflare Tunnel to a local server or Nabu Casa requires changing only the `HA_BASE_URL` environment variable — no code changes.

### Entity organization by HA areas

Group devices on the dashboard by HA's native area assignments (living room, bedroom, etc.) rather than by entity type. This matches how non-technical users think about their home.

**Fallback**: Entities without area assignments are grouped under "Other".

## Risks / Trade-offs

- **Polling latency** → State updates depend on polling interval (default 5s). Users may see stale states for up to 5 seconds. Acceptable for lights and AC; would be problematic for security-critical devices (not in scope).
- **Vercel cold starts** → First request after idle may take 1-3 seconds. Mitigated by Vercel's automatic keep-warm on free tier for frequently visited pages.
- **Cloudflare Access + API proxy** → Every server-side request from Vercel to HA goes through Cloudflare Access. The Route Handler must include a valid Cloudflare Access service token or bypass configuration to avoid OTP challenges on server-to-server calls.
- **HA API versioning** → HA REST API is stable but not formally versioned. A HA update could break the dashboard. Mitigated by pinning to well-documented endpoints (`/api/states`, `/api/services`).
