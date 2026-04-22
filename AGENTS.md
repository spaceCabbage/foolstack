# AI Assistant Instructions for Foolstack Projects

This document provides specific instructions for Gemini, Claude, or other AI assistants working on projects based on the Foolstack template (Django + Vue3 + Redis + PostgreSQL dockerized application).

## Project Overview

This is a full-stack web application with:
- **Backend**: Django REST API
- **Frontend**: Vue3 SPA (PWA supported)
- **Background Tasks**: Django 6.0 Native Tasks (Threaded)
- **Cache/Session**: Redis
- **Database**: PostgreSQL 16
- **Infrastructure**: Docker, Caddy reverse proxy

## Key Architecture Decisions

1. **Single Domain Routing**: All traffic goes through Caddy on a single domain
   - `/api/*` → Django backend
   - `/admin/*` → Django admin
   - `/static/*` → Static files
   - `/*` → Vue frontend

2. **SSL Everywhere**: HTTPS enabled in both dev (self-signed) and production (Let's Encrypt)

3. **Docker Compose Overlays**:
   - `docker-compose.yml` - Production-safe base config
   - `docker-compose.dev.yml` - Development overrides (hot reload, port exposure)

4. **Non-root Containers**: Server runs as `appuser` (UID 1000) for security

5. **Data Directory**: All persistent data in `./data/` with proper permissions

6. **Identity & Persistence**:
   - Models inherit from `core.models.BaseModel` using **ULID** primary keys.
   - Time-sortable, 26-character unique identifiers.

## Working with the Codebase

### Environment Variables

Key variables in `.env`:

```env
# Required
PROJECT_NAME=foolstack          # Used for container/volume naming
ENVIRONMENT=development         # development or production
DOMAIN=localhost                # Your domain (serves SPA + API)
SECRET_KEY=...                  # Django secret key (auto-generated)

# Database
POSTGRES_DB=foolstack
POSTGRES_USER=foolstack
POSTGRES_PASSWORD=foolstack

# Optional (with sensible defaults)
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR, CRITICAL
CADDY_EMAIL=admin@example.com   # Let's Encrypt email (production)

# Ports (all have defaults - configure if needed)
CADDY_HTTP_PORT=80              # External HTTP port
CADDY_HTTPS_PORT=443            # External HTTPS port
SERVER_PORT=8000                # Django internal port
CLIENT_PORT=5173                # Vite dev / 80 in prod
REDIS_PORT=6379                 # Redis internal port
```

### Service Names

- `server` - Django backend
- `client` - Vue frontend
- `redis` - Redis cache/session
- `db` - PostgreSQL database
- `caddy` - Reverse proxy

Container names are prefixed with PROJECT_NAME (e.g., `foolstack_server`)

### File Paths

- Django project: `/app` in container, `./server` on host
- Vue project: `/app` in container, `./client` on host
- Data directory: `/data` in container, `./data` on host
- Database: Managed by Docker volumes (`db_data`)
- Static files: `/data/staticfiles`
- Media files: `/data/mediafiles`
- Logs: `/data/logs`

## Makefile Commands

### Setup & Lifecycle
- `make setup` - First-time setup (creates .env, builds, installs deps via `uv` and `bun`)
- `make up` - Start services (auto-detects dev/prod mode)
- `make down` - Stop services
- `make restart` - Restart all services
- `make build` - Build Docker images
- `make build-clean` - Build without cache

### Development
- `make deps` - Sync local Python venv (`uv`) + Bun dependencies (for IDE)
- `make shell` - Django shell
- `make logs [FLAGS]` - View logs (s=server, c=client, r=redis, d=caddy)
- `make status` - Show system status and health
- `make urls` - Show access URLs

### Database
- `make migrations` - Create Django migrations
- `make migrate` - Apply migrations
- `make superuser` - Create admin user

### Testing
- `make test` - Run all tests
- `make test-coverage` - Run tests with coverage report

### Project Management
- `make init <name>` - Rename project from template
- `make purge` - Nuclear option: wipe everything

## Adding New Features

### Creating Django Apps
```bash
make manage startapp myapp
```
Then add to `INSTALLED_APPS` in `server/core/settings.py`

### Adding API Endpoints
1. Inherit models from `core.models.BaseModel`.
2. Create serializers in `server/myapp/serializers.py`
3. Create views in `server/myapp/views.py`
4. Add URLs: `path("api/myapp/", include("myapp.urls"))` in `server/core/urls.py`

### Background Tasks (Django 6.0)
```python
# server/myapp/tasks.py
from django.tasks import task

@task()
def my_background_task(arg):
    # Do something
    return result

# Usage:
# my_background_task.enqueue("some_arg")
```

### Frontend Auth (JWT)
- Store: `client/src/stores/auth.js` (Pinia)
- API Client: `client/src/apiClient/client.js` (Axios with interceptors for token refresh)

## Auth Endpoints

The template ships with **registration and password reset disabled by default** for security.
Enable them by uncommenting in `server/users/urls.py`.

**Enabled by default:**
- `POST /api/auth/login/` - Returns JWT `access` and `refresh` tokens.
- `POST /api/auth/token/refresh/` - Refresh JWT access token.
- `GET/PUT /api/auth/profile/` - View/update user profile (authenticated).

**Email Configuration:**
- Development: Emails logged to console AND enqueued to threaded task.
- Production: Set `RESEND_API_KEY` for delivery.

## Health Endpoints

- `/api/ping/` - Fast healthcheck (database only) - used by Docker
- `/api/health/` - Comprehensive check (database, Redis, disk space)

## Production Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Update `DOMAIN` to your actual domain
3. Ensure `SECRET_KEY` is secure
4. Run `make up` - Caddy auto-provisions SSL via Let's Encrypt

## File Structure

```
foolstack/
├── server/
│   ├── core/              # Django project settings
│   │   ├── tasks.py       # Threaded task backend
│   │   ├── models.py      # BaseModel (ULID)
│   │   ├── settings.py    # Main config
│   │   └── urls.py        # URL routing
│   ├── users/             # User auth app
│   ├── pyproject.toml     # Python deps (uv)
│   └── Dockerfile
├── client/
│   ├── src/               # Vue source
│   ├── package.json       # JS deps (bun)
│   ├── Caddyfile          # Production SPA routing
│   └── Dockerfile
├── data/                  # Persistent data (gitignored except .gitkeep)
│   ├── logs/
│   ├── staticfiles/
│   ├── mediafiles/
│   ├── caddy_data/
│   └── caddy_config/
├── docker-compose.yml     # Production config
├── docker-compose.dev.yml # Development overrides
├── Caddyfile              # Main reverse proxy config
├── Makefile               # All commands
└── .env.example           # Environment template
```

## AI Assistant Best Practices

1. **Use Makefile commands** - Don't use raw docker-compose
2. **Check existing patterns** before implementing new features
3. **All API routes under `/api/`** - Caddy routes based on path
4. **Background tasks via Django 6.0 Tasks** - Don't use Celery or raw threading.
5. **Test in Docker** - The local venv is only for IDE support
6. **Update AGENTS.md** when adding significant features
