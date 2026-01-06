from django.contrib import admin
from django.urls import include, path

from .health import health_check, ping

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/ping/", ping, name="ping"),
    path("api/health/", health_check, name="health_check"),
    path("api/auth/", include("users.urls")),
]
