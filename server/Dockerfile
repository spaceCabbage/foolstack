# Multi-stage build for optimal caching and performance
FROM python:3.13.5-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# System dependencies layer (cached until Dockerfile changes)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (cached until Poetry version changes)
RUN pip install poetry==1.7.1

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Dependencies installation layer (cached until pyproject.toml/poetry.lock changes)
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev && rm -rf $POETRY_CACHE_DIR

# Development stage
FROM base AS development

# Install dev dependencies
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