FROM python:3.13.5-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directoryc
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY req.txt ./

# Install Python dependencies (this layer will be cached unless req.txt changes)
RUN pip install --no-cache-dir -r req.txt

# Copy project files (this won't invalidate the pip install cache)
COPY . .

# Create directories for data and logs inside /app
RUN mkdir -p /app/data /app/logs

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Run different commands based on environment
CMD ["sh", "-c", "if [ \"$ENVIRONMENT\" = \"development\" ]; then python manage.py migrate && python manage.py runserver 0.0.0.0:8000; else python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-30} --keepalive ${GUNICORN_KEEPALIVE:-2} --max-requests ${GUNICORN_MAX_REQUESTS:-1000} --max-requests-jitter ${GUNICORN_MAX_REQUESTS_JITTER:-100} --preload --access-logfile - --error-logfile -; fi"]