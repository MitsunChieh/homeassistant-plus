## 1. Cloudflare Tunnel connectivity

- [x] 1.1 Add Cloudflared add-on repository (`https://github.com/homeassistant-apps/repository`) to HA Add-on Store
- [x] 1.2 Install Cloudflared add-on (v7.0.5) on HA Supervisor
- [x] 1.3 Configure Cloudflare Tunnel connectivity: set external hostname `homeassistant.mitsun.cc` in the add-on settings
- [x] 1.4 Enable Watchdog for automatic restart on crash (tunnel auto-recovery)
- [x] 1.5 Enable auto-update for the Cloudflared add-on
- [x] 1.6 Authorize Cloudflare account via the auth URL in the add-on logs

## 2. Reverse Proxy Trust

- [x] 2.1 Install File Editor add-on on HA for editing configuration files
- [x] 2.2 Add `http` section to `configuration.yaml` with `use_x_forwarded_for: true` and `trusted_proxies: 172.30.33.0/24`
- [x] 2.3 Reboot HA to apply the reverse proxy trust configuration

## 3. Cloudflare Access authentication

- [x] 3.1 Set up Cloudflare Zero Trust account with team name and free plan (50 users)
- [x] 3.2 Set up Cloudflare Access authentication: create Access Application (Self-hosted) for `homeassistant.mitsun.cc` with 1-week session duration
- [x] 3.3 Create Access Policy (Allow Teammate) with authorized email address for OTP verification
- [x] 3.4 Verify unauthenticated requests return HTTP 302 redirect to Cloudflare login
- [x] 3.5 Verify authorized email receives OTP and grants access to HA after authentication
