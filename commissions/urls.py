from django.urls import path

from .views import *

urlpatterns = [
    path("requests", CommissionListView.as_view(), name="requests"),
    path("request/<int:pk>", CommissionDetailView.as_view(), name="request-detail"),
]

app_name = "commissions"
