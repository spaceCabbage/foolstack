from django.contrib import admin
from django.urls import path, include

from .health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("api/v1/auth/", include("users.urls")),
]
