from django.urls import path
from .views import event_list, event_detail

urlpatterns = [
    path('localevents/events/', event_list, name='event-list'),
    path('localevents/event/<int:pk>/', event_detail, name='event-detail'),
]

app_name = "localevents"