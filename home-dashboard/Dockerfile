ARG BUILD_FROM=node:20-alpine

FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY src/ src/
COPY next.config.ts tsconfig.json postcss.config.mjs ./
COPY public/ public/
RUN npm run build

FROM ${BUILD_FROM}

RUN apk add --no-cache nodejs npm bash curl

# Install bashio for HA add-on options parsing
RUN curl -sL https://github.com/hassio-addons/bashio/archive/refs/tags/v0.16.2.tar.gz | tar xz \
    && mv bashio-0.16.2/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    && rm -rf bashio-0.16.2

WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
COPY run.sh /

EXPOSE 3000
CMD ["/run.sh"]
