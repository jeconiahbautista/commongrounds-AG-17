from django.contrib import admin
from .models import Project, ProjectCategory

class ProjectInline(admin.TabularInline):
    model = Project

class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInline, ]
    ordering = ['name']

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    ordering = ['created_on']
    search_fields = ('title', 'description')
    list_display = ('title', 'category', 'description', 'created_on', 'updated_on')

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
