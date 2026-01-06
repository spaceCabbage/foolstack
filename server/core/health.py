import os
import time

import redis
from django.conf import settings
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def ping(request):
    """Fast healthcheck - database connection only.

    Used by Docker healthchecks and load balancers.
    Should be as fast as possible.
    """
    try:
        connection.ensure_connection()
        return Response({"status": "ok", "database": "connected"})
    except Exception:
        return Response(
            {"status": "error", "database": "disconnected"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Comprehensive health check.

    Checks database, Redis, disk space, and reports environment info.
    Used by monitoring dashboards.
    """
    start_time = time.time()

    health = {
        "status": "healthy",
        "version": getattr(settings, "VERSION", "unknown"),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "checks": {},
    }

    # Check database
    try:
        db_start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health["checks"]["database"] = {
            "status": "healthy",
            "response_time_ms": round((time.time() - db_start) * 1000, 2),
        }
    except Exception as e:
        health["status"] = "unhealthy"
        health["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e),
        }

    # Check Redis
    try:
        redis_start = time.time()
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        health["checks"]["redis"] = {
            "status": "healthy",
            "response_time_ms": round((time.time() - redis_start) * 1000, 2),
        }
    except Exception as e:
        health["status"] = "unhealthy"
        health["checks"]["redis"] = {
            "status": "unhealthy",
            "error": str(e),
        }

    # Check disk space (data directory)
    try:
        data_path = "/data"
        if os.path.exists(data_path):
            stat = os.statvfs(data_path)
            free_space_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
            health["checks"]["disk_space"] = {
                "status": "healthy" if free_space_mb > 100 else "warning",
                "free_space_mb": round(free_space_mb, 2),
            }
        else:
            health["checks"]["disk_space"] = {
                "status": "warning",
                "message": "Data directory not found",
            }
    except Exception as e:
        health["checks"]["disk_space"] = {
            "status": "warning",
            "error": str(e),
        }

    health["response_time_ms"] = round((time.time() - start_time) * 1000, 2)

    status_code = (
        status.HTTP_200_OK
        if health["status"] == "healthy"
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return Response(health, status=status_code)
