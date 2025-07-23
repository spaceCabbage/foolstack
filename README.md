# 🚀 foolstack - Modern Django + Vue3 Dockerized Stack

A production-ready full-stack application template featuring Django REST API, Vue3 SPA, and Caddy reverse proxy and more - all containerized with Docker.

## ✨ Features

- **🐍 Django REST API Backend** - Robust API with Django REST Framework
- **⚡ Vue3 + Vite Frontend** - Lightning-fast modern frontend
- **🔒 Caddy Reverse Proxy** - Automatic HTTPS with Let's Encrypt
- **🐳 Docker Everything** - Fully containerized for consistency
- **🔄 Hot Reload** - Development with live code updates
- **🌍 Environment-Based Config** - Single `.env` file controls everything
- **📦 Production Ready** - Optimized builds for deployment


## 📋 Prerequisites

- Docker & Docker Compose
- Git
- Make (optional but recommended)

## 🚀 Quick Start

### For New Developers - One Command Setup

```bash
# Clone and setup everything automatically
git clone https://github.com/spaceCabbage/foolstack
cd foolstack
make setup
```

This will:
- Create `.env` with secure defaults
- Generate a random Django secret key
- Build all Docker containers
- Start the services
- Run database migrations
- Prompt you to create a superuser

### Manual Setup (Alternative)

```bash
# Clone the repository
git clone <your-repo-url>
cd foolstack

# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env

# Build and start all services
make build
make up

# Run migrations
make migrate

# Create admin user
make superuser
```

### 4. Access Your App

- **Frontend**: http://localhost (or https://yourdomain.com)
- **API**: http://api.localhost (or https://api.yourdomain.com)
- **Django Admin**: http://api.localhost/admin

## 🛠️ Development Workflow

### Common Commands

```bash
# View all available commands
make help

# Start/stop services
make up
make down

# View logs
make logs

# Django operations
make migrate       # Run migrations
make migration     # Create new migrations
make superuser     # Create admin user

# Access containers
make shell-django  # Django shell
make shell-vue     # Vue shell

# Development
make dev-django-shell  # Django Python shell
make dev-install       # Install Vue dependencies
```

## 🚢 Production Deployment

### 1. Prepare Environment

```bash
# Update .env for production
ENVIRONMENT=production
BASE_DOMAIN=yourdomain.com
DJANGO_SECRET_KEY=generate-a-secure-key
DJANGO_DEBUG=False
CADDY_EMAIL=your-email@domain.com
```

### 2. Deploy

```bash
# Build production images
make prod-build

# Start production services
make prod-up

# Run migrations
make migrate
```
