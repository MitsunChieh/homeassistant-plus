ARG BUILD_FROM
FROM ${BUILD_FROM} AS base

# HA base image already includes bashio and s6-overlay
RUN apk add --no-cache nodejs npm

# ---- Build stage ----
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY src/ src/
COPY next.config.ts tsconfig.json postcss.config.mjs ./
RUN npm run build

# ---- Runtime ----
FROM base
WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Install s6 service definition (let s6-overlay manage the process, not override CMD)
COPY rootfs/ /
RUN chmod +x /etc/s6-overlay/s6-rc.d/dashboard/run

EXPOSE 8099
