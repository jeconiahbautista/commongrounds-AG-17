from django.urls import path
from .views import (
    register_view,
    permission_denied_view,
    ProfileUpdateView,
    CustomLoginView,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", register_view, name="register"),
    path("permission-denied/", permission_denied_view, name="permission_denied"),
    path(
        "profiles/<str:username>/", ProfileUpdateView.as_view(), name="profile_update"
    ),
]

app_name = "accounts"
