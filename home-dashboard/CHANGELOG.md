# Changelog

## 0.1.1 - 2026-04-08

- Remove `public/` directory copy from Dockerfile (caused build failure because the empty directory is not tracked by git)
- Sync `EXPOSE` port with runtime `PORT` (8099)

## 0.1.0 - 2026-04-04

- Initial release
- Next.js App Router dashboard with area-based device grouping
- Supported entities: lights, temperature sensors, humidity sensors, climate
- Server-side HA REST API proxy with SWR polling (5s interval)
- HA ingress support
