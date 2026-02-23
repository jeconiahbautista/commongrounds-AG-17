from django.contrib import admin

from .models import Commission, CommissionType

class CommissionInline(admin.TabularInline):
    model = Commission

class CommissionTypeAdmin(admin.ModelAdmin):
    inlines = [CommissionInline, ]

class CommissionAdmin(admin.ModelAdmin):
    model = Commission

    search_fields = ('title', )

    list_display = ('title', 'description', 'people_required', 'updated_on', 'created_on' )

    list_filter = ('updated_on', )

    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'people_required'), 
                'commission_type',
                'description',
            ]
        }),
    ]

admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
