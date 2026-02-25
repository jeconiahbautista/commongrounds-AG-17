from django.urls import path
from .views import diyprojects_list

urlpatterns = [
    path('diyprojects', diyprojects_list, name='diyprojects_list'),
]