FROM python:3.13-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    SERVER_PORT=8000

WORKDIR /app

# Create non-root user (UID 1000 matches most Linux users)
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser && \
    chown -R appuser:appuser /app

FROM base AS dependencies

COPY requirements.txt ./

# Create venv with copies (not symlinks) for IDE compatibility
RUN python3 -m venv --copies /app/.venv && \
    /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install -r requirements.txt

FROM base AS development

COPY --chown=appuser:appuser --from=dependencies /app/.venv /app/.venv
COPY --chown=appuser:appuser . .

ENV PATH="/app/.venv/bin:$PATH"

# Create data directories with proper ownership
RUN mkdir -p /data/staticfiles /data/mediafiles /data/logs && \
    chown appuser:appuser /data /data/staticfiles /data/mediafiles /data/logs

USER appuser
EXPOSE ${SERVER_PORT}

CMD sh -c "python manage.py runserver 0.0.0.0:${SERVER_PORT}"

FROM base AS production

COPY --chown=appuser:appuser --from=dependencies /app/.venv /app/.venv
COPY --chown=appuser:appuser . .

ENV PATH="/app/.venv/bin:$PATH"

# Create data directories with proper ownership
RUN mkdir -p /data/staticfiles /data/mediafiles /data/logs && \
    chown appuser:appuser /data /data/staticfiles /data/mediafiles /data/logs

# Collect static files
RUN python manage.py collectstatic --noinput || true

USER appuser
EXPOSE ${SERVER_PORT}

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${SERVER_PORT}/api/ping/ || exit 1

CMD sh -c "gunicorn core.wsgi:application --bind 0.0.0.0:${SERVER_PORT} --workers 3 --threads 2 --worker-class gthread --max-requests 1000 --max-requests-jitter 50 --timeout 60 --access-logfile - --error-logfile - --log-level info"
