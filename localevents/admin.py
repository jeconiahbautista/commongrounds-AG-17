from django.contrib import admin

from .models import Event, EventType, EventSignup


class EventInLine(admin.StackedInline):
    model = Event


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    inlines = [
        EventInLine,
    ]


class EventSignupInline(admin.TabularInline):
    model = EventSignup


class EventAdmin(admin.ModelAdmin):
    model = Event
    search_fields = (
        "title",
        "category",
        "location",
        "start_time",
        "end_time",
    )
    list_display = (
        "title",
        "category",
        "event_image",
        "location",
        "description",
        "start_time",
        "end_time",
        "event_capacity",
        "status",
        "updated_on",
        "created_on",
    )
    list_filter = ("category",)

    inlines = [EventSignupInline]

    fieldsets = [
        (
            "Details",
            {
                "fields": [
                    (
                        "title",
                        "category",
                        "organizer",
                        "event_image",
                        "location",
                        "description",
                    ),
                    (
                        "start_time",
                        "end_time",
                        "event_capacity",
                        "status",
                    ),
                ]
            },
        )
    ]


class EventSignupAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "user_registrant",
        "new_registrant",
    )

    search_fields = ("event__title",)


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventSignup, EventSignupAdmin)
