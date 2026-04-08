#!/usr/bin/env bash
set -e

# Read HA token from add-on options
HA_TOKEN=$(bashio::config 'ha_token')
export HA_TOKEN
export HA_BASE_URL="http://homeassistant:8123"

cd /app
exec node server.js
