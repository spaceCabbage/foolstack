# Claude Assistant Instructions for Foolstack Projects

This document provides specific instructions for Claude or other AI assistants working on projects based on the Foolstack template (Django + Vue3 + Redis + Celery dockerized application).

## Project Overview

This is a full-stack web application with:
- **Backend**: Django REST API
- **Frontend**: Vue3 SPA
- **Worker**: Celery for background tasks
- **Cache/Broker**: Redis
- **Infrastructure**: Docker, Caddy reverse proxy, SQLite database

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

## Working with the Codebase

### Environment Variables

Key variables in `.env`:

```env
PROJECT_NAME=foolstack          # Used for container/volume naming
ENVIRONMENT=development         # development or production
SERVER_DOMAIN=localhost         # Your domain
SECRET_KEY=...                  # Django secret key (auto-generated)
REDIS_URL=redis://redis:6379/0  # Redis connection
CELERY_BROKER_URL=redis://...   # Celery broker
```

### Service Names

- `server` - Django backend
- `worker` - Celery worker
- `client` - Vue frontend
- `redis` - Redis cache/broker
- `caddy` - Reverse proxy

Container names are prefixed with PROJECT_NAME (e.g., `foolstack_server`)

### File Paths

- Django project: `/app` in container, `./server` on host
- Vue project: `/app` in container, `./client` on host
- Data directory: `/data` in container, `./data` on host
- Database: `/data/db.sqlite3`
- Static files: `/data/staticfiles`
- Media files: `/data/mediafiles`
- Logs: `/data/logs`

## Makefile Commands

### Setup & Lifecycle
- `make setup` - First-time setup (creates .env, builds, installs deps)
- `make up` - Start services (auto-detects dev/prod mode)
- `make down` - Stop services
- `make restart` - Restart all services
- `make build` - Build Docker images
- `make build-clean` - Build without cache

### Development
- `make deps` - Sync local Python venv + Bun dependencies (for IDE)
- `make shell` - Django shell
- `make logs [FLAGS]` - View logs (s=server, c=client, w=worker, r=redis, d=caddy)
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
make shell
python manage.py startapp myapp
```
Then add to `INSTALLED_APPS` in `server/core/settings.py`

### Adding API Endpoints
1. Create serializers in `server/myapp/serializers.py`
2. Create views in `server/myapp/views.py`
3. Add URLs: `path("api/myapp/", include("myapp.urls"))` in `server/core/urls.py`

### Creating Celery Tasks
```python
# server/myapp/tasks.py
from celery import shared_task

@shared_task
def my_background_task(arg):
    # Do something
    return result
```

### Frontend API Calls
```javascript
// Use relative paths - Caddy proxies /api/* to Django
fetch('/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
})
```

## Health Endpoints

- `/api/ping/` - Fast healthcheck (database only) - used by Docker
- `/api/health/` - Comprehensive check (database, Redis, disk space)

## Production Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Update `SERVER_DOMAIN` to your actual domain
3. Ensure `SECRET_KEY` is secure
4. Run `make up` - Caddy auto-provisions SSL via Let's Encrypt

## File Structure

```
foolstack/
├── server/
│   ├── core/              # Django project settings
│   │   ├── settings.py    # Main config
│   │   ├── celery.py      # Celery setup
│   │   ├── health.py      # Health endpoints
│   │   └── urls.py        # URL routing
│   ├── users/             # User auth app
│   ├── requirements.txt   # Python deps
│   └── Dockerfile
├── client/
│   ├── src/               # Vue source
│   ├── package.json       # JS deps
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
4. **Background tasks via Celery** - Don't use threading or async for long tasks
5. **Test in Docker** - The local venv is only for IDE support
6. **Update CLAUDE.md** when adding significant features

## Common Issues

1. **Connection refused**: Check if services are running with `make status`
2. **Permission errors**: Data directory needs proper permissions (handled by `make up`)
3. **SSL warnings**: Expected in dev - accept the self-signed certificate
4. **Hot reload not working**: Check `CHOKIDAR_USEPOLLING` is set in dev overlay
