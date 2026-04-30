from django.urls import path
from .views import permission_denied_view, ProfileUpdateView

urlpatterns = [
    path("permission-denied/", permission_denied_view, name="permission_denied"),
    path("profile/<str:username>/", ProfileUpdateView.as_view(), name="profile_update"),
]

app_name = "accounts"
