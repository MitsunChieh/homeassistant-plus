# remote-access Specification

## Purpose

TBD - created by archiving change 'setup-remote-access'. Update Purpose after archive.

## Requirements

### Requirement: Cloudflare Tunnel connectivity

The system SHALL provide external access to Home Assistant via a Cloudflare Tunnel, without opening any ports on the local network router.

#### Scenario: External access via tunnel

- **WHEN** a user navigates to `https://homeassistant.mitsun.cc` from outside the local network
- **THEN** the request SHALL be routed through the Cloudflare Tunnel to the local HA instance

#### Scenario: Tunnel auto-recovery

- **WHEN** the Cloudflared add-on crashes or becomes unresponsive
- **THEN** the Watchdog SHALL automatically restart the add-on to restore connectivity

---
### Requirement: Reverse proxy trust

The system SHALL accept forwarded requests from the Cloudflared container by trusting the `172.30.33.0/24` subnet as a reverse proxy in HA's HTTP configuration.

#### Scenario: Forwarded request accepted

- **WHEN** a request arrives from the Cloudflared container with `X-Forwarded-For` headers
- **THEN** HA SHALL accept the request and use the original client IP from the forwarded headers

#### Scenario: Untrusted proxy rejected

- **WHEN** a request with `X-Forwarded-For` headers arrives from an IP outside `172.30.33.0/24`
- **THEN** HA SHALL reject the forwarded headers and treat the request source as the direct IP

---
### Requirement: Cloudflare Access authentication

The system SHALL require Cloudflare Access (Zero Trust) email OTP authentication before any external request reaches Home Assistant.

#### Scenario: Unauthenticated request blocked

- **WHEN** an unauthenticated user navigates to `https://homeassistant.mitsun.cc`
- **THEN** Cloudflare Access SHALL redirect to an email OTP login page

#### Scenario: Authorized email receives OTP

- **WHEN** a user enters an email address listed in the Access policy
- **THEN** Cloudflare SHALL send a one-time PIN to that email address

#### Scenario: Unauthorized email rejected

- **WHEN** a user enters an email address not listed in the Access policy
- **THEN** Cloudflare Access SHALL deny access and display a block page

#### Scenario: Authenticated session duration

- **WHEN** a user completes OTP verification
- **THEN** the session SHALL remain valid for 1 week before requiring re-authentication
