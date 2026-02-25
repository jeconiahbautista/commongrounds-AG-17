from django.urls import path
from .views import diyprojects_list

urlpatterns = [
    path('projects', diyprojects_list, name='diyprojects_list'),
    path('project', diyprojects_list, name='diyprojects_list'),
]

app_name = 'diyprojects'