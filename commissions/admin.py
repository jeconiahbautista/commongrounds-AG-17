from django.contrib import admin

from .models import Commission, CommissionType


class CommissionInline(admin.TabularInline):
    model = Commission


class CommissionTypeAdmin(admin.ModelAdmin):
    inlines = [CommissionInline]


class CommissionAdmin(admin.ModelAdmin):
    search_fields = ("title",)

    list_display = (
        "title",
        "type",
        "maker",
        "people_required",
        "status",
        "created_on",
        "updated_on",
    )

    list_filter = (
        "status",
        "type",
        "created_on",
        "updated_on",
    )

    readonly_fields = ("created_on", "updated_on")

    fieldsets = [
        (
            "Details",
            {
                "fields": [
                    ("title", "people_required"),
                    "type",
                    "maker",
                    "status",
                    "description",
                ]
            },
        ),
    ]


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)