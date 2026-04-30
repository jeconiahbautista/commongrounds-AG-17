from django.urls import path
from .views import event_list, event_detail, event_create, event_edit, EventSignupView

urlpatterns = [
    path("events/", event_list, name="event-list"),
    path("event/<int:pk>/", event_detail, name="event-detail"),
    path("event/add/", event_create, name="event-create"),
    path("event/<int:pk>/edit/", event_edit, name="event-detail-edit"),
    path(
        "event/<int:pk>/signup/", EventSignupView.as_view(), name="event-detail-signup"
    ),
]

app_name = "localevents"
