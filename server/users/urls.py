from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

# fmt:off
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    # path("register/", views.RegisterView.as_view(), name="register"),
    # path("password-reset/", views.PasswordResetRequestView.as_view(), name="password_reset_request"),
    # path("password-reset/confirm/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
