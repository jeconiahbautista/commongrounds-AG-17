from django.contrib import admin
from .models import Project, ProjectCategory

class ProjectCategoryInline(admin.TabularInline):
    model = ProjectCategory

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    inlines = []

class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
