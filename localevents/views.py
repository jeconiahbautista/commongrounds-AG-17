from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Event, EventSignup
from .forms import EventForm
from accounts.decorators import role_required


def event_list(request):
    events = Event.objects.all()

    created_events = []
    signed_events = []

    if request.user.is_authenticated:
        profile = request.user.profile

        created_events = Event.objects.filter(organizer=profile)
        signed_events = Event.objects.filter(events__user_registrant=profile)

        excluded = created_events | signed_events
        events = events.exclude(id__in=excluded)

    ctx = {
        "events": events,
        "created_events": created_events,
        "signed_events": signed_events,
    }

    return render(request, "event-list.html", ctx)


def event_detail(request, pk):
    event = Event.objects.get(pk=pk)

    is_organizer = False
    is_full = False

    if request.user.is_authenticated:
        profile = request.user.profile
        is_organizer = profile in event.organizer.all()

    signup_count = event.events.count()
    is_full = signup_count >= event.event_capacity

    ctx = {
        "event": event,
        "is_organizer": is_organizer,
        "is_full": is_full,
    }

    return render(request, "event-detail.html", ctx)


@login_required
@role_required("Event Organizer")
def event_create(request):
    form = EventForm()

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save()
            event.organizer.add(request.user.profile)

            return redirect("localevents:event-list")

    ctx = {"form": form}

    return render(request, "event-form.html", ctx)


@login_required
@role_required("Event Organizer")
def event_edit(request, pk):
    event = Event.objects.get(pk=pk)

    if request.user.profile not in event.organizer.all():
        return redirect("localevents:event-list")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            event = form.save(commit=False)

            signup_count = event.events.count()
            if signup_count >= event.event_capacity:
                event.status = "Full"
            else:
                event.status = "Available"

            event.save()

            return redirect(event.get_absolute_url())

        else:
            form = EventForm(instance=event)

        ctx = {"form": form, "event": event}

    return render(request, "event-form.html", ctx)


def event_signup(request, pk):
    event = Event.objects.get(pk=pk)

    if request.user.is_authenticated:
        profile = request.user.profile

        EventSignup.objects.create(event=event, user_registrant=profile)

        return redirect(event.get_absolute_url())

    if request.method == "POST":
        name = request.POST.get("name")

        EventSignup.objects.create(event=event, new_registrant=name)

        return redirect(event.get_absolute_url())

    return render(request, "event-signup.html", {"event": event})
