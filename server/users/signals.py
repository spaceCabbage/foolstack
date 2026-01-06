"""
Authentication event signals for logging.
Logs successful logins, failed login attempts, and logouts.
"""

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver
from loguru import logger


def get_client_ip(request):
    """Extract client IP from request, handling proxy headers."""
    if request is None:
        return "unknown"
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log successful user login."""
    ip = get_client_ip(request)
    logger.info(
        "User login: {user} from {ip}",
        user=user.email or user.username,
        ip=ip,
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log user logout."""
    if user is None:
        return
    ip = get_client_ip(request)
    logger.info(
        "User logout: {user} from {ip}",
        user=user.email or user.username,
        ip=ip,
    )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """Log failed login attempt."""
    ip = get_client_ip(request)
    # Only log username/email, never the password
    username = credentials.get("username", credentials.get("email", "unknown"))
    logger.warning(
        "Failed login attempt: {username} from {ip}",
        username=username,
        ip=ip,
    )
