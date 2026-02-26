from django.contrib import admin

from .models import Event, EventType

class EventInLine(admin.StackedInline):
    model = Event

class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    inlines = [EventInLine,]

class EventAdmin(admin.ModelAdmin):
    model = Event
    search_fields = ('title','location',)
    list_display = ('title', 'category', 'location', 'description', 'start_time','end_time','updated_on','created_on')
    list_filter = ('category',)
    fieldsets = [
        ('Details', {
            'fields':[
                ('title', 'category', 'location', 'description',), ('start_time','end_time'),
            ]
        })
    ]

admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
# Register your models here.
