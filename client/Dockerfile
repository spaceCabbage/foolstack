# Bun-based multi-stage build for ultra-fast installs
FROM oven/bun:1.2-alpine AS base

WORKDIR /app

# Dependencies layer (cached until package.json/bun.lockb changes)
COPY package.json bun.lockb* ./
RUN bun install --frozen-lockfile

# Development stage
FROM base AS development

ENV NODE_ENV=development \
    CLIENT_PORT=5173

# Copy source code (changes frequently)
COPY . .

# Expose the Vite dev server port
EXPOSE ${CLIENT_PORT}

# Start development server with host binding for Docker
CMD sh -c "bun run dev -- --host 0.0.0.0 --port ${CLIENT_PORT}"

# Build stage - builds the Vue app
FROM base AS build

ENV NODE_ENV=production

COPY . .

# Build the application
RUN bun run build

# Production stage - serves with Caddy
FROM caddy:2-alpine AS production

ENV CLIENT_PORT=80

# Copy built assets from build stage
COPY --from=build /app/dist /app/dist

# Copy Caddyfile for SPA routing
COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE ${CLIENT_PORT}

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
