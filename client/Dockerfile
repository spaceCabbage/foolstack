# Development stage - Vite dev server
FROM node:lts-slim AS development

# Set environment variables
ENV NODE_ENV=development

# Set work directory
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies (including dev dependencies)
RUN npm ci --silent && npm cache clean --force

# Copy source code
COPY . .

# Expose the configurable Vite port
EXPOSE ${VUE_PORT:-5173}

# Start development server with host binding for Docker
CMD ["sh", "-c", "npm run dev -- --host 0.0.0.0 --port ${VUE_PORT:-5173}"]

# Production stage - Build and serve static files
FROM node:lts-slim AS production

# Set environment variables
ENV NODE_ENV=production

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies needed for build
RUN npm ci --silent && npm cache clean --force

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Simple file server for production (Caddy handles the actual serving)
# This container just needs to build and make files available
CMD ["sh", "-c", "echo 'Built successfully. Files ready in /app/dist' && sleep infinity"]