"""
FoolStack Template - Created by Yehuda Freedman
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

from .logging import setup_logging

VERSION = "1.0.0"
PROJECT_NAME = os.getenv("PROJECT_NAME", "foolstack")


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default-key-change-in-production")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT != "production"
DOMAIN = os.getenv("DOMAIN", "localhost")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

if ENVIRONMENT == "development":
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "server", DOMAIN]
else:
    ALLOWED_HOSTS = [DOMAIN, f"www.{DOMAIN}"]


if ENVIRONMENT == "development":
    CSRF_TRUSTED_ORIGINS = [
        f"https://{DOMAIN}",
        f"https://localhost",
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
        f"https://{DOMAIN}",
        f"https://www.{DOMAIN}",
    ]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
ROOT_URLCONF = "core.urls"
STATIC_URL = "/static/"
STATIC_ROOT = "/data/staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = "/data/mediafiles"
LOGS_DIR = "/data/logs"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.RequestLoggingMiddleware",
]


# Logging
setup_logging()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "default": {
            "class": "core.logging.InterceptHandler",
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["default"],
    },
    "loggers": {
        "django": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "celery": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database - SQLite by default
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/" + os.getenv("DATABASE_NAME", "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Custom user model
AUTH_USER_MODEL = "users.User"

# ========================================
# Redis Configuration
# ========================================
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ========================================
# Celery Configuration
# ========================================
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# ========================================
# REST Framework Configuration
# ========================================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "EXCEPTION_HANDLER": "core.exceptions.custom_exception_handler",
}

# JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# ========================================
# Security Settings (Production)
# ========================================
if ENVIRONMENT == "production":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = [r"^api/ping/$", r"^api/health/$"]
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
