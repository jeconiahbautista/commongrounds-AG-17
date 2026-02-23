from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('requests', RequestListView.as_view(), name="requests" )
]

app_name = "commissions"