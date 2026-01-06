# Bun-based multi-stage build for ultra-fast installs
FROM oven/bun:1 AS base

WORKDIR /app

# Dependencies layer (cached until package.json/bun.lockb changes)
COPY package.json bun.lockb* ./
RUN bun install --frozen-lockfile

# Development stage
FROM base AS development

ENV NODE_ENV=development

# Copy source code (changes frequently)
COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Start development server with host binding for Docker
CMD ["bun", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

# Build stage - builds the Vue app
FROM base AS build

ENV NODE_ENV=production

COPY . .

# Build the application
RUN bun run build

# Production stage - serves with Caddy
FROM caddy:2-alpine AS production

# Copy built assets from build stage
COPY --from=build /app/dist /app/dist

# Copy Caddyfile for SPA routing
COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE 80

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
