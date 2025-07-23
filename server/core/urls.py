from django.contrib import admin
from django.urls import path

from .health import health_check, readiness_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("ready/", readiness_check, name="readiness_check"),
]
