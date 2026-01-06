# ========================================
# Foolstack Makefile
# ========================================
# Project management commands for Foolstack (Django + Vue3 + Redis + Celery)

.PHONY: help setup build build-clean up down restart logs status urls shell migrations migrate superuser collectstatic deps manage test test-coverage purge init

# Variables
PROJECT_NAME := $(shell grep -E '^PROJECT_NAME=' .env 2>/dev/null | cut -d '=' -f2 || echo "foolstack")

# Default target - show help
help:
	@echo "Foolstack - Django + Vue3 + Redis + Celery"
	@echo ""
	@echo "-> New here? Just run 'make setup'"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          - First-time setup (creates .env, builds, installs deps)"
	@echo "  make up             - Start services (detached)"
	@echo "  make down           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs [FLAGS]   - Follow logs (run 'make logs h' for service flags)"
	@echo "  make status         - Show system status and health"
	@echo "  make urls           - Show access URLs"
	@echo "  make shell          - Open Django shell (interactive Python)"
	@echo ""
	@echo "  make build          - Build Docker images"
	@echo "  make build-clean    - Build Docker images without cache"
	@echo "  make migrations     - Create Django migrations"
	@echo "  make migrate        - Run database migrations"
	@echo "  make superuser      - Create Django superuser"
	@echo "  make collectstatic  - Collect static files (for production)"
	@echo "  make purge          - DANGER: Wipes database, volumes and images"
	@echo ""
	@echo "  make deps           - Sync local venv with requirements.txt"
	@echo "  make manage <cmd>   - Run any Django management command"
	@echo ""
	@echo "  make test           - Run all tests"
	@echo "  make test-coverage  - Run tests with coverage report"
	@echo ""
	@echo "  make init <name>    - Initialize new project from template (rename)"

# Sync local Python and Bun dependencies (for VSCode/IDE)
deps:
	@echo "=========================================="
	@echo "Syncing Dependencies"
	@echo "=========================================="
	@echo ""
	@echo "📦 Syncing Python dependencies..."
	@if [ ! -d server/.venv ]; then \
		echo "⚠️  Local venv doesn't exist. Creating it..."; \
		cd server && python3 -m venv --copies .venv; \
	fi
	@cd server && .venv/bin/pip install --upgrade pip -q
	@cd server && .venv/bin/pip install -r requirements.txt
	@echo "✅ Python venv updated"
	@echo ""
	@echo "📦 Syncing Bun dependencies..."
	@cd client && bun install --frozen-lockfile 2>/dev/null || cd client && bun install
	@echo "✅ Bun dependencies synced"
	@echo ""
	@echo "💡 Run 'make build' to update Docker images"

# Show access URLs
urls:
	@ENVIRONMENT=$$(grep -E '^ENVIRONMENT=' .env 2>/dev/null | cut -d '=' -f2 || echo "development"); \
	DOMAIN=$$(grep -E '^DOMAIN=' .env 2>/dev/null | cut -d '=' -f2 || echo "localhost"); \
	echo "Access URLs:"; \
	echo "  Frontend:  https://$$DOMAIN"; \
	echo "  API:       https://$$DOMAIN/api"; \
	echo "  Admin:     https://$$DOMAIN/admin"; \
	echo "  Health:    https://$$DOMAIN/api/health"

# Show comprehensive system status
status:
	@echo "=========================================="
	@echo "$(PROJECT_NAME) System Status"
	@echo "=========================================="
	@ENVIRONMENT=$$(grep -E '^ENVIRONMENT=' .env 2>/dev/null | cut -d '=' -f2 || echo "development"); \
	echo "Environment: $$ENVIRONMENT"
	@echo ""
	@echo "--- Containers ---"
	@docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.RunningFor}}" 2>/dev/null || echo "No containers running (run 'make up' to start)"
	@echo ""
	@if docker-compose ps 2>/dev/null | grep -q "Up"; then \
		echo "--- Health Check ---"; \
		curl -sk https://localhost/api/health/ 2>/dev/null | python3 -c "import sys, json; data = json.load(sys.stdin); print(f\"Status: {'✅' if data.get('status') == 'healthy' else '❌'} {data.get('status', 'unknown').upper()}\"); checks = data.get('checks', {}); print(f\"Database: {'✅' if checks.get('database', {}).get('status') == 'healthy' else '❌'}\"); print(f\"Redis: {'✅' if checks.get('redis', {}).get('status') == 'healthy' else '❌'}\")" 2>/dev/null || echo "Status: ❌ Unable to fetch health status"; \
	fi

# First-time setup with proper SECRET_KEY generation
setup:
	@echo "=========================================="
	@echo "Foolstack First-Time Setup"
	@echo "=========================================="
	@echo ""
	@if [ ! -f .env ]; then \
		echo "📄 Copying .env.example to .env..."; \
		cp .env.example .env; \
		echo "🔐 Generating SECRET_KEY..."; \
		if command -v python3 >/dev/null 2>&1; then \
			SECRET_KEY=$$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))'); \
		else \
			SECRET_KEY=$$(openssl rand -base64 50 | tr -d '\n'); \
		fi; \
		if [ -n "$$SECRET_KEY" ]; then \
			sed -i.bak "s|^SECRET_KEY=.*|SECRET_KEY=$$SECRET_KEY|" .env && rm -f .env.bak; \
			echo "✅ Generated secure SECRET_KEY"; \
		else \
			echo "❌ Failed to generate SECRET_KEY. Please set it manually in .env"; \
			exit 1; \
		fi; \
		echo "✅ .env file created successfully"; \
	else \
		echo "✅ .env file already exists, skipping..."; \
		echo "   To regenerate, delete .env and run 'make setup' again"; \
	fi
	@echo ""
	@echo "📦 Installing local dependencies (Python + Bun)..."
	@$(MAKE) deps
	@echo ""
	@echo "📁 Creating data directories with proper permissions..."
	@mkdir -p data/logs data/mediafiles data/staticfiles data/caddy_data data/caddy_config
	@chmod 777 data/logs data/mediafiles data/staticfiles data/caddy_data data/caddy_config
	@echo "✅ Data directories created"
	@echo ""
	@echo "🐳 Building Docker images..."
	@$(MAKE) build
	@echo ""
	@echo "=========================================="
	@echo "✅ Setup Complete!"
	@echo "=========================================="
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run 'make up' to start all services"
	@echo "  2. Run 'make migrate' to apply database migrations"
	@echo "  3. Run 'make superuser' to create an admin user"
	@echo ""
	@echo "Access point: https://localhost"
	@echo ""
	@echo "Note: Development uses HTTPS with self-signed certificate."
	@echo "      Accept the certificate warning in your browser."

# Build Docker images
build:
	@echo "Building Docker images..."
	@docker-compose build

# Build Docker images without cache
build-clean:
	@echo "Building Docker images (no cache)..."
	@docker-compose build --no-cache

# Start services (automatically adapts to ENVIRONMENT from .env)
up:
	@mkdir -p data/logs data/mediafiles data/staticfiles data/caddy_data data/caddy_config
	@chmod 777 data/logs data/mediafiles data/staticfiles data/caddy_data data/caddy_config 2>/dev/null || true
	@ENVIRONMENT=$$(grep -E '^ENVIRONMENT=' .env | cut -d '=' -f2 || echo "development"); \
	echo "Starting services in $$ENVIRONMENT mode..."; \
	if [ "$$ENVIRONMENT" = "production" ]; then \
		docker-compose up -d; \
	else \
		docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d; \
	fi
	@echo ""
	@$(MAKE) urls
	@echo ""
	@echo "Run 'make logs' to view logs"

# Stop services (handles both dev and prod)
down:
	@echo "Stopping services..."
	@docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
	@echo "✅ Services stopped"

# Restart all services (down + up)
restart:
	@echo "Restarting all services..."
	@$(MAKE) down
	@$(MAKE) up

# View logs with optional service flags
# Usage:
#   make logs        → all services
#   make logs s      → server only
#   make logs scw    → server, client, worker
#   make logs h      → show help
# Flags: s (server), c (client), w (worker), r (redis), d (caddy)
logs:
	@ARGS="$(filter-out $@,$(MAKECMDGOALS))"; \
	SERVICES=""; \
	if [ -z "$$ARGS" ]; then \
		echo "Following all logs (Ctrl+C to exit)..."; \
		docker-compose logs -f; \
	elif [ "$$ARGS" = "h" ] || [ "$$ARGS" = "help" ] || [ "$$ARGS" = "-h" ] || [ "$$ARGS" = "--help" ]; then \
		echo "Usage: make logs [FLAGS]"; \
		echo "make logs         All services (default)"; \
		echo ""; \
		echo "View logs from specific services by combining flag characters:"; \
		echo "  s  Server (Django backend)"; \
		echo "  c  Client (Vue frontend)"; \
		echo "  w  Worker (Celery worker)"; \
		echo "  r  Redis"; \
		echo "  d  Caddy (reverse proxy)"; \
		echo ""; \
		echo "Examples:"; \
		echo "  make logs sw       Watch server and worker"; \
		echo "  make logs scw      Watch frontend, backend, and worker"; \
	else \
		case "$$ARGS" in \
			*s*) SERVICES="$$SERVICES server";; \
		esac; \
		case "$$ARGS" in \
			*c*) SERVICES="$$SERVICES client";; \
		esac; \
		case "$$ARGS" in \
			*w*) SERVICES="$$SERVICES worker";; \
		esac; \
		case "$$ARGS" in \
			*r*) SERVICES="$$SERVICES redis";; \
		esac; \
		case "$$ARGS" in \
			*d*) SERVICES="$$SERVICES caddy";; \
		esac; \
		if [ -z "$$SERVICES" ]; then \
			echo "❌ Unknown flags: $$ARGS"; \
			echo ""; \
			echo "Run 'make logs h' for usage help"; \
		else \
			echo "Following logs for:$$SERVICES (Ctrl+C to exit)..."; \
			docker-compose logs -f $$SERVICES; \
		fi; \
	fi

# Open Django shell
shell:
	@echo "Opening Django shell..."
	@docker-compose exec server python manage.py shell

# Create Django migrations
migrations:
	@echo "Creating Django migrations..."
	@docker-compose exec server python manage.py makemigrations

# Run Django migrations
migrate:
	@echo "Running Django migrations..."
	@docker-compose exec server python manage.py migrate

# Create Django superuser
superuser:
	@echo "Creating superuser (interactive mode)..."
	@docker-compose exec -it server python manage.py createsuperuser

# Collect static files (for production)
collectstatic:
	@echo "Collecting static files..."
	@docker-compose exec server python manage.py collectstatic --noinput
	@echo "✅ Static files collected to data/staticfiles/"

# Generic Django management command pass-through
manage:
	@docker-compose exec server python manage.py $(filter-out $@,$(MAKECMDGOALS))

# Catch-all target to prevent make errors when passing arguments
%:
	@:

# Run all tests
test:
	@echo "Running all tests..."
	@docker-compose exec server python -m pytest $(filter-out $@,$(MAKECMDGOALS))

# Run tests with coverage report
test-coverage:
	@echo "Running tests with coverage..."
	@docker-compose exec server python -m pytest --cov=. --cov-report=html --cov-report=term
	@echo ""
	@echo "✅ Coverage report generated at server/htmlcov/index.html"

# Nuclear option - fresh slate
purge:
	@echo "WARNING: This will delete ALL data, volumes, and images!"
	@echo "Press Ctrl+C within 5 seconds to cancel..."
	@sleep 5
	@echo ""
	@echo "Stopping services..."
	@docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v
	@echo "Removing volumes..."
	@docker volume rm $(PROJECT_NAME)_redis_data 2>/dev/null || true
	@echo "Removing generated files (keeping .gitkeep)..."
	@find data -type f ! -name '.gitkeep' -delete 2>/dev/null || true
	@echo ""
	@echo "Purge complete! Run 'make setup' to start fresh."

# Initialize new project from template (rename)
init:
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ]; then \
		echo "Error: Please specify a project name using 'make init myproject'"; \
		exit 1; \
	fi
	@echo "🔄 Initializing project as $(word 2,$(MAKECMDGOALS))..."
	@$(eval LOWERCASE := $(word 2,$(MAKECMDGOALS)))
	@$(eval UPPERCASE := $(shell echo $(word 2,$(MAKECMDGOALS)) | tr '[:lower:]' '[:upper:]'))
	@$(eval CAPITALIZED := $(shell echo $(word 2,$(MAKECMDGOALS)) | sed 's/^./\u&/'))
	@find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.vue" -o -name "*.html" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.toml" -o -name "*.txt" -o -name "*.env*" -o -name "Makefile" -o -name "Dockerfile*" -o -name "Caddyfile*" \) \
		-not -path "./server/.venv/*" \
		-not -path "./client/node_modules/*" \
		-not -path "./.git/*" \
		-not -path "./data/*" \
		-exec sed -i.bak \
			-e 's/foolstack/$(LOWERCASE)/g' \
			-e 's/Foolstack/$(CAPITALIZED)/g' \
			-e 's/FOOLSTACK/$(UPPERCASE)/g' {} \; 2>/dev/null || \
	find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.vue" -o -name "*.html" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.toml" -o -name "*.txt" -o -name "*.env*" -o -name "Makefile" -o -name "Dockerfile*" -o -name "Caddyfile*" \) \
		-not -path "./server/.venv/*" \
		-not -path "./client/node_modules/*" \
		-not -path "./.git/*" \
		-not -path "./data/*" \
		-exec sed -i '' \
			-e 's/foolstack/$(LOWERCASE)/g' \
			-e 's/Foolstack/$(CAPITALIZED)/g' \
			-e 's/FOOLSTACK/$(UPPERCASE)/g' {} \;
	@find . -name "*.bak" -type f -delete 2>/dev/null || true
	@echo "✅ Project renamed to $(word 2,$(MAKECMDGOALS))!"
	@echo ""
	@echo "📝 Next steps:"
	@echo "   1. Run 'make setup' to complete initialization"
	@echo "   2. Update git remote if needed"
