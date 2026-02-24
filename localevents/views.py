from django.shortcuts import render
from .models import Event

def event_list(request):
    events = Event.objects.all()

    ctx = {
        "events": events
    }

    return render(request, "event-list.html", ctx)

def event_detail(request, pk):
    event = Event.objects.get(pk=pk)

    ctx = {
        "event": event
    }

    return render(request, "event-detail.html", ctx)

# Create your views here.
