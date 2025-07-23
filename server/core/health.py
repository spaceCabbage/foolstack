import os
import time
from django.http import JsonResponse
from django.db import connection
from django.conf import settings


def health_check(request):
    """
    Health check endpoint that verifies:
    - Database connectivity
    - Application status
    - Environment information
    """
    start_time = time.time()
    health_data = {
        "status": "healthy",
        "timestamp": int(time.time()),
        "environment": getattr(settings, 'ENVIRONMENT', 'unknown'),
        "version": getattr(settings, 'VERSION', 'unknown'),
        "checks": {}
    }
    
    # Database health check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_data["checks"]["database"] = {
                "status": "healthy",
                "response_time_ms": round((time.time() - start_time) * 1000, 2)
            }
    except Exception as e:
        health_data["status"] = "unhealthy"
        health_data["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Disk space check (data directory)
    try:
        data_path = getattr(settings, 'BASE_DIR', '/app') / 'data'
        if os.path.exists(data_path):
            stat = os.statvfs(data_path)
            free_space_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
            health_data["checks"]["disk_space"] = {
                "status": "healthy" if free_space_mb > 100 else "warning",
                "free_space_mb": round(free_space_mb, 2)
            }
        else:
            health_data["checks"]["disk_space"] = {
                "status": "warning",
                "message": "Data directory not found"
            }
    except Exception as e:
        health_data["checks"]["disk_space"] = {
            "status": "warning",
            "error": str(e)
        }
    
    # Overall response time
    health_data["response_time_ms"] = round((time.time() - start_time) * 1000, 2)
    
    # Return appropriate HTTP status
    status_code = 200 if health_data["status"] == "healthy" else 503
    
    return JsonResponse(health_data, status=status_code)


def readiness_check(request):
    """
    Readiness check - simpler check for load balancers
    """
    return JsonResponse({"status": "ready"}, status=200)