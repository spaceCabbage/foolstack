# Claude Assistant Instructions for Gelt Project

This document provides specific instructions for Claude or other AI assistants working on this Django + Vue3 dockerized project.

## Project Overview

This is a full-stack web application with:
- **Backend**: Django REST API at `api.{BASE_DOMAIN}`
- **Frontend**: Vue3 SPA at `{BASE_DOMAIN}`
- **Infrastructure**: Docker, Caddy reverse proxy, SQLite database

## Key Architecture Decisions

1. **Single .env Configuration**: All services read from root `.env` file
2. **Domain-based Routing**: Frontend at base domain, API at `api.` subdomain
3. **Environment Detection**: `ENVIRONMENT` variable switches between dev/prod behavior
4. **SQLite Database**: Stored in `./data/` directory with volume mounting

## Working with the Codebase

### Environment Variables

The entire stack is controlled by these key variables in `.env`:

```env
ENVIRONMENT=development|production  # Controls debug mode, CORS, etc.
BASE_DOMAIN=localhost              # Base for all domain configuration
CLIENT_PORT=3000                   # Vue dev server port (referenced as VUE_PORT)
```

### Service Names

When referencing containers in commands or configurations:
- Django container: `server` (container name: `gelt_server`)
- Vue container: `client` (container name: `gelt_client`)
- Caddy container: `caddy` (container name: `gelt_caddy`)

### File Paths

- Django project root: `/app` inside container, `./server` on host
- Vue project root: `/app` inside container, `./client` on host
- Database location: `/app/data/db.sqlite3` inside Django container

## Common Tasks

### Initial Setup for New Developers

The `make setup` command automates the entire development setup:

1. Checks if `.env` exists (won't overwrite)
2. Creates `.env` with:
   - Auto-generated secure Django secret key using Python's `secrets` module
   - Development environment settings
   - Localhost as base domain
3. Builds all Docker containers
4. Starts services
5. Runs Django migrations
6. Provides instructions for creating superuser

This eliminates manual configuration errors and ensures consistent development environments.

### Adding Django Apps

1. Create app in server directory:
```bash
make shell-django
cd /app
python manage.py startapp appname
```

2. Update `INSTALLED_APPS` in `server/core/settings.py`

### Adding API Endpoints

1. Create serializers in `server/appname/serializers.py`
2. Create viewsets in `server/appname/views.py`
3. Register URLs in `server/core/urls.py`

### Frontend API Integration

API calls from Vue should use relative paths:
```javascript
// In development, Vite proxy handles /api/* routes
fetch('/api/endpoint')  // Proxied to Django

// Or use the configured API URL
const apiUrl = import.meta.env.VITE_API_URL
```

## Important Configuration Details

### CORS Settings

CORS is automatically configured based on environment:
- **Development**: Allows `localhost:3000`, `BASE_DOMAIN:3000`
- **Production**: Allows `https://BASE_DOMAIN`, `https://www.BASE_DOMAIN`

### Django Settings

- `DEBUG` is automatically `True` in development, `False` in production
- `ALLOWED_HOSTS` includes Django container name for internal Docker networking
- Static files are collected to `/app/staticfiles` in production

### Makefile Commands

Custom commands have been simplified:
- `make migration` → runs `makemigrations`
- `make superuser` → runs `createsuperuser`

## Security Considerations

When working on this project:

1. **Never commit .env file** - It's gitignored for a reason
2. **Generate new SECRET_KEY** for production deployments
3. **Review CORS settings** before deploying
4. **Default REST permissions** are `AllowAny` - implement proper authentication

## Development Workflow

1. **Quick Start**: Use `make setup` for automatic development environment setup
2. **VSCode Integration**: Run `make vscode-setup` to create local Python venv for IDE features
3. **Hot Reload**: Both Django and Vue auto-reload on file changes
4. **Database Migrations**: Always run `make migrate` after model changes
5. **Dependencies**: Update `pyproject.toml` or `package.json`, then rebuild containers

### Dual Environment Setup

This project uses a dual environment approach:
- **Local .venv**: Created by `make vscode-setup` for VSCode Python interpreter and intellisense
- **Docker**: Uses system Python (no venv) to avoid volume mount conflicts

Both environments use the same Poetry dependencies, ensuring consistency.

## Production Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Update `BASE_DOMAIN` to actual domain
3. Caddy will auto-provision SSL certificates
4. Consider switching to PostgreSQL for production

## Debugging Tips

1. **Check Logs**: `make logs` shows all container output
2. **Network Issues**: Services communicate using container names (server, client, caddy)
3. **Permission Errors**: Data directory might need ownership fix
4. **CORS Errors**: Check if domains match in `.env` and browser URL
5. **Setup Issues**: The `make setup` command handles most initial configuration automatically

## Testing

- Django tests: `make test`
- Vue tests: `make shell-vue` then `npm run test`

## File Structure Conventions

```
server/
├── core/           # Django project settings
├── apps/           # Django applications
├── static/         # Static files (if any)
└── req.txt         # Python dependencies

client/
├── src/
│   ├── components/ # Vue components
│   ├── views/      # Vue pages
│   └── api/        # API integration
└── package.json    # Node dependencies
```

## Notes for Modifications

1. **Dockerfile Changes**: Rebuild with `make build`
2. **Environment Changes**: Restart with `make restart`
3. **Database Schema**: Run migrations after model changes
4. **New Dependencies**: Update req.txt/package.json and rebuild

Remember: This setup prioritizes developer experience with hot-reload and simple configuration while remaining production-ready.