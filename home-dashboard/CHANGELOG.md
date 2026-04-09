# Changelog

## 0.1.4 - 2026-04-08

- Set `init: false` in `config.yaml` so HA Supervisor doesn't wrap the container with its own init. This lets s6-overlay run as PID 1 (required by the HA base image).

## 0.1.3 - 2026-04-08

- Fix `s6-overlay-suexec: fatal: can only run as pid 1` crash on startup
- Run Next.js server as an s6-overlay longrun service instead of overriding CMD
- Use bashio to read `ha_token` option (instead of jq)

## 0.1.2 - 2026-04-08

- Use HA official base image (`ghcr.io/home-assistant/{arch}-base`) instead of `node:20-alpine`
- Remove manual bashio installation (already included in HA base image)
- Install only `nodejs` and `npm` packages at runtime

## 0.1.1 - 2026-04-08

- Remove `public/` directory copy from Dockerfile (caused build failure because the empty directory is not tracked by git)
- Sync `EXPOSE` port with runtime `PORT` (8099)

## 0.1.0 - 2026-04-04

- Initial release
- Next.js App Router dashboard with area-based device grouping
- Supported entities: lights, temperature sensors, humidity sensors, climate
- Server-side HA REST API proxy with SWR polling (5s interval)
- HA ingress support
