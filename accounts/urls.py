from django.urls import path
from .views import (
    dashboard,
    seller_dashboard,
    permission_denied_view,
    ProfileUpdateView,
)

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("seller-dashboard/", seller_dashboard, name="seller_dashboard"),
    path("permission-denied/", permission_denied_view, name="permission_denied"),
    path("<str:username>/", ProfileUpdateView.as_view(), name="profile_update"),
]

app_name = "accounts"
