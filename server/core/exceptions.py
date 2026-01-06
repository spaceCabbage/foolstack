"""
Custom DRF exception handler with logging.
Provides consistent error responses and logs all API errors.
"""

from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Handle exceptions with logging and consistent response format.

    Logs:
    - All API exceptions with context
    - Distinguishes between client errors (4xx) and server errors (5xx)

    Returns:
    - Consistent JSON response format with 'error' key
    """
    response = exception_handler(exc, context)

    request = context.get("request")
    view = context.get("view")

    if request:
        method = request.method
        path = request.path
        user = str(request.user) if hasattr(request, "user") else "unknown"
    else:
        method = path = user = "unknown"

    view_name = view.__class__.__name__ if view else "unknown"

    if response is not None:
        status_code = response.status_code

        if status_code >= 500:
            logger.error(
                "API Error [{status}] {method} {path} in {view} [{user}]: {exc}",
                status=status_code,
                method=method,
                path=path,
                view=view_name,
                user=user,
                exc=str(exc),
            )
        elif status_code >= 400:
            logger.warning(
                "API Error [{status}] {method} {path} in {view} [{user}]: {exc}",
                status=status_code,
                method=method,
                path=path,
                view=view_name,
                user=user,
                exc=str(exc),
            )

        if isinstance(response.data, dict):
            if "detail" not in response.data and "error" not in response.data:
                response.data = {"error": response.data}
        elif isinstance(response.data, list):
            response.data = {"errors": response.data}
        else:
            response.data = {"error": str(response.data)}

    else:
        logger.exception(
            "Unhandled API exception in {method} {path} ({view}) [{user}]: {exc}",
            method=method,
            path=path,
            view=view_name,
            user=user,
            exc=str(exc),
        )

        response = Response(
            {"error": "An unexpected error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
