from django.urls import path

from .views import CommissionDetailView, CommissionListView, CommissionCreateView, CommissionUpdateView, apply_to_job

urlpatterns = [
    path("requests/", CommissionListView.as_view(), name="request-list"),
    path("request/add/", CommissionCreateView.as_view(), name="request-add"),
    path("request/<int:pk>/", CommissionDetailView.as_view(), name="request-detail"),
    path("request/<int:pk>/edit/", CommissionUpdateView.as_view(), name="request-edit"),
    path("job/<int:pk>/apply/", apply_to_job, name="job-apply"),
]

app_name = "commissions"
