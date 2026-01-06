"""
Custom middleware for Django.
Includes request logging with timing and structured data.
"""

import time

from loguru import logger


class RequestLoggingMiddleware:
    """Log all HTTP requests with timing and context.

    Logs:
    - Request method and path
    - Response status code
    - Request duration in ms
    - User info (if authenticated)
    - Client IP

    In development: logs at DEBUG level for 2xx, INFO for others
    In production: logs at INFO level for all requests
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip health check endpoints to avoid log noise
        if request.path in ["/api/ping/", "/api/health/"]:
            return self.get_response(request)

        start_time = time.time()

        # Get client IP (handle proxy headers)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.META.get("REMOTE_ADDR", "unknown")

        # Process request
        response = self.get_response(request)

        # Calculate duration
        duration_ms = round((time.time() - start_time) * 1000, 2)

        # Get user info
        user = "anonymous"
        if hasattr(request, "user") and request.user.is_authenticated:
            user = str(request.user)

        # Build log message
        status_code = response.status_code
        method = request.method
        path = request.path

        log_data = {
            "method": method,
            "path": path,
            "status": status_code,
            "duration_ms": duration_ms,
            "user": user,
            "ip": client_ip,
        }

        # Choose log level based on status code
        if status_code >= 500:
            logger.error(
                "{method} {path} → {status} ({duration_ms}ms) [{user}@{ip}]",
                **log_data,
            )
        elif status_code >= 400:
            logger.warning(
                "{method} {path} → {status} ({duration_ms}ms) [{user}@{ip}]",
                **log_data,
            )
        else:
            logger.info(
                "{method} {path} → {status} ({duration_ms}ms) [{user}@{ip}]",
                **log_data,
            )

        return response

    def process_exception(self, request, exception):
        """Log unhandled exceptions before they propagate."""
        logger.exception(
            "Unhandled exception in {method} {path}: {exc}",
            method=request.method,
            path=request.path,
            exc=str(exception),
        )
        return None
