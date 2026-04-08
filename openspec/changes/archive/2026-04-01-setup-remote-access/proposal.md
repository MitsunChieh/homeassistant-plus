## Why

Home Assistant runs on an Odroid N2 (aarch64) on the local network. To build a custom dashboard accessible from the internet — and to allow remote management — HA needs a secure external access path without opening router ports or modifying the device OS.

## What Changes

- Install Cloudflared add-on (v7.0.5) on HA Supervisor to establish a Cloudflare Tunnel
- Configure `homeassistant.mitsun.cc` as the external hostname routed through the tunnel
- Add `http.trusted_proxies` to HA `configuration.yaml` to accept requests from the Cloudflared container (`172.30.33.0/24`)
- Set up Cloudflare Access (Zero Trust) with email OTP authentication to protect the external endpoint
- Enable Watchdog and auto-update on the Cloudflared add-on for reliability

## Non-Goals

- **Nabu Casa**: Rejected — $75/year for functionality achievable for free with Cloudflare Tunnel add-on, since HA Supervisor supports add-ons
- **Port forwarding / DDNS**: Rejected — exposes ports directly, larger attack surface
- **Tailscale**: Rejected — requires client installation on every accessing device, not suitable for general users
- **Modifying the Odroid N2 OS directly**: The device is treated as appliance-only; all changes go through HA Supervisor add-ons

## Capabilities

### New Capabilities

- `remote-access`: Secure external access to Home Assistant via Cloudflare Tunnel and Cloudflare Access (Zero Trust) authentication

### Modified Capabilities

(none)

## Impact

- HA configuration: `configuration.yaml` — added `http` section with `use_x_forwarded_for` and `trusted_proxies`
- HA add-ons: Cloudflared (v7.0.5) installed and configured
- Cloudflare: Tunnel created for `homeassistant.mitsun.cc`, Access application with email OTP policy
- DNS: `homeassistant.mitsun.cc` CNAME managed by Cloudflare Tunnel
