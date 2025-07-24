# Bun-based multi-stage build for ultra-fast installs
FROM oven/bun:1 AS base

WORKDIR /app

# Dependencies layer (cached until package.json/bun.lockb changes)
COPY package.json bun.lockb* ./
RUN bun install --frozen-lockfile

# Development stage
FROM base AS development

# Set environment variables
ENV NODE_ENV=development

# Copy source code (changes frequently)
COPY . .

# Expose the configurable Vite port
EXPOSE ${VUE_PORT:-5173}

# Start development server with host binding for Docker
CMD ["sh", "-c", "bun run dev -- --host 0.0.0.0 --port ${VUE_PORT:-5173}"]

# Production stage - Build static files
FROM base AS production

# Set environment variables
ENV NODE_ENV=production

# Copy source code
COPY . .

# Build the application
RUN bun run build

# Simple completion indicator for production
CMD ["sh", "-c", "echo 'Built successfully. Files ready in /app/dist' && sleep infinity"]