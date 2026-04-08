ARG BUILD_FROM
FROM ${BUILD_FROM} AS base

# HA base image already includes bashio, we only need Node.js
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
COPY run.sh /

EXPOSE 8099
CMD ["/run.sh"]
