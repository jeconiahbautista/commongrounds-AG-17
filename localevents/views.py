from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponseForbidden

from accounts.decorators import role_required
from .models import Event, EventSignup
from .forms import EventForm


def event_list(request):
    events = Event.objects.all()

    created_events = []
    signed_events = []

    if request.user.is_authenticated:
        profile = request.user.profile

        created_events = Event.objects.filter(organizer=profile)
        signed_events = Event.objects.filter(signups__user_registrant=profile)

        excluded_ids = list(created_events.values_list("id", flat=True)) + list(
            signed_events.values_list("id", flat=True)
        )

        events = events.exclude(id__in=excluded_ids)

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
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        profile = request.user.profile
        is_organizer = profile in event.organizer.all()

    signup_count = event.signups.all().count()
    is_full = signup_count >= event.event_capacity

    ctx = {
        "event": event,
        "is_organizer": is_organizer,
        "is_full": is_full,
        "is_authenticated": is_authenticated,
    }

    return render(request, "event-detail.html", ctx)


@login_required
@role_required("Event Organizer")
def event_create(request):
    form = EventForm(user=request.user)

    if request.method == "POST":
        form = EventForm(request.POST or None, request.FILES or None, user=request.user)

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

    form = EventForm(
        request.POST or None, request.FILES or None, instance=event, user=request.user
    )
    form.fields["status"].disabled = True

    if request.method == "POST" and form.is_valid():
        event = form.save(commit=False)

        signup_count = event.signups.count()

        if event.status not in ["Done", "Cancelled"]:
            if signup_count >= event.event_capacity:
                event.status = "Full"
            else:
                event.status = "Available"

        event.save()

        return redirect(event.get_absolute_url())

    return render(request, "event-form.html", {"form": form, "event": event})


# def event_signup(request, pk):
#     event = Event.objects.get(pk=pk)

#     if request.user.is_authenticated:
#         profile = request.user.profile

#         EventSignup.objects.create(event=event, user_registrant=profile)

#         return redirect("localevents:event-list")

#     if request.method == "POST":
#         name = request.POST.get("name")

#         EventSignup.objects.create(event=event, new_registrant=name)

#         return redirect("localevents:event-list")

#     return render(request, "event-signup.html", {"event": event})


class BaseSignupView(View):
    def post(self, request, pk):
        event = self.get_event(pk)

        if not self.check_capacity(event):
            return HttpResponseForbidden("Event is full")

        if not self.can_signup(event, request.user):
            return HttpResponseForbidden("You cannot sign up to your own event")

        self.create_signup(event, request)

        return redirect(self.get_redirect_url(event))

    def get(self, request, pk):
        event = self.get_event(pk)
        return render(request, "event-signup.html", {"event": event})

    def get_event(self, pk):
        raise NotImplementedError

    def check_capacity(self, event):
        raise NotImplementedError

    def can_signup(self, event, user):
        raise NotImplementedError

    def create_signup(self, event, request):
        raise NotImplementedError

    def get_redirect_url(self, event):
        raise NotImplementedError


class EventSignupView(BaseSignupView):
    def get_event(self, pk):
        return Event.objects.get(pk=pk)

    def check_capacity(self, event):
        return event.signups.count() < event.event_capacity

    def can_signup(self, event, user):
        if not user.is_authenticated:
            return True
        return user.profile not in event.organizer.all()

    def create_signup(self, event, request):
        if request.user.is_authenticated:
            EventSignup.objects.get_or_create(
                event=event, user_registrant=request.user.profile
            )
        else:
            name = request.POST.get("name")
            EventSignup.objects.create(event=event, new_registrant=name)

    def get_redirect_url(self, event):
        return "localevents:event-list"
