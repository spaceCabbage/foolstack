# Multi-stage build for optimal caching and performance
FROM python:3.13.5-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Minimal system dependencies - most Python packages are now wheel-based
# Only install if you add packages requiring compilation later

# Install Poetry and (required for pkg_resources in Python 3.13+)
RUN pip install poetry==2.1.3 

# Configure Poetry - use system Python to avoid venv issues with volume mounts
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Dependencies installation layer (cached until pyproject.toml/poetry.lock changes)
COPY pyproject.toml poetry.lock* ./
RUN poetry install --only main && rm -rf $POETRY_CACHE_DIR

# Development stage
FROM base AS development

# Install all dependencies (including dev)
RUN poetry install && rm -rf $POETRY_CACHE_DIR

# Copy source code (this layer changes frequently)
COPY . .

# Create directories
RUN mkdir -p /app/data /app/logs

# Development command
CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py runserver 0.0.0.0:8000"]

# Production stage
FROM base AS production

# Copy source code
COPY . .

# Create directories
RUN mkdir -p /app/data /app/logs

# Collect static files
RUN poetry run python manage.py collectstatic --noinput || true

# Production command
CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-30} --keepalive ${GUNICORN_KEEPALIVE:-2} --max-requests ${GUNICORN_MAX_REQUESTS:-1000} --max-requests-jitter ${GUNICORN_MAX_REQUESTS_JITTER:-100} --preload --access-logfile - --error-logfile -"]