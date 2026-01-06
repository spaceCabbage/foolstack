"""
Custom throttle classes for auth endpoints.
Uses Redis cache backend for distributed rate limiting.
"""

from rest_framework.throttling import ScopedRateThrottle


class LoginRateThrottle(ScopedRateThrottle):
    """Throttle for login attempts - 5 per minute per IP."""

    scope = "login"


class RegisterRateThrottle(ScopedRateThrottle):
    """Throttle for registration - 3 per minute per IP."""

    scope = "register"


class PasswordResetRateThrottle(ScopedRateThrottle):
    """Throttle for password reset requests - 3 per minute per IP."""

    scope = "password_reset"
