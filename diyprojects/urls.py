from django.urls import path
from .views import diyprojects_list, diyprojects_detail

urlpatterns = [
    path('projects/', diyprojects_list, name='diyprojects_list'),
    path('project/<int:pk>/', diyprojects_detail, name='diyprojects_detail'),
]

app_name = 'diyprojects'