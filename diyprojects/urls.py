from django.urls import path
from .views import diyprojects_list, diyprojects_detail, diyprojects_edit

urlpatterns = [
    path("projects/", diyprojects_list, name="diyprojects_list"),
    path("project/<int:pk>/", diyprojects_detail, name="diyprojects_detail"),
    path("project/<int:pk>/edit", diyprojects_edit, name="diyprojects_edit"),
]

app_name = "diyprojects"
